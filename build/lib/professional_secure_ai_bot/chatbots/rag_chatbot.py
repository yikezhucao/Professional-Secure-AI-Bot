from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from professional_secure_ai_bot.ai_tools.ai_llm import get_llm
from professional_secure_ai_bot.ai_tools.embedder import get_embedder

# 新增依赖
# from professional_secure_ai_bot.chatbots.base_chatbot import chatbot_answer  # 基础聊天机器人工具调用能力
# from professional_secure_ai_bot.tools.file_management import (
#     get_file_content,
#     get_filenames_in_directory,
#     delete_file,
#     create_file,
# )

llm = get_llm()

embedder = get_embedder()


def rag_answer(question: str) -> str:
    """Uses the base_chatbot.py to implement a chatbot that can access a vectorstore."""
    vectorstore = Chroma(embedding_function=embedder, persist_directory="./chroma_db")

    # Retrieve and generate using the relevant snippets of the text.
    retriever = vectorstore.as_retriever()
    prompt = PromptTemplate.from_template(
        """
        You are a network operations AI assistant based on Retrieval-Augmented Generation (RAG), dedicated to answering user questions related to network troubleshooting and diagnostics.

        Use the following context to answer the user's question. 
        - DO NOT fabricate answers.
        - DO NOT provide private or sensitive information (e.g., ip address, usernames, passwords).
        - If the answer is not available in the context, reply: "抱歉，我不能回答这个问题。"

        Question: {question}

        Context: 
        {context}

        Answer:

        """
    )
    # prompt = PromptTemplate.from_template()
    #     """You are a network operations AI assistant based on Retrieval-Augmented Generation (RAG), dedicated to answering user questions related to network operations.
    #     Answer the following question {question} by using the following context. 
    #     DO NOT ANSWER PRIVATE INFORMATION.
    #     DO NOT ANSWER USER NAME AND PASSWORD.
    #     If the answer is not in the context or this prompt, say "抱歉，我无法回答这个问题。"
    
    #     Question: {question}

    #     Context: {context}
    #     Answer:
    
    #     """
    # )

    # prompt = PromptTemplate.from_template(
    #     """你是一个基于检索增强生成（RAG）的网络运维AI助手，致力于回答用户提出的网络运维问题。
    #     请根据上下文{context}，回答问题{question}。
    #     请勿回答隐私信息。
    #     请勿回答用户名密码。
    #     如果答案不在上下文中，请说"抱歉，我无法回答这个问题。"
        
    #     问题：{question}
        
    #     上下文：{context}

    #     答案：
    #     """
    # )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(question)

# def rag_answer(question: str, tools: list = None) -> str:
#     """增强版 RAG 答案生成器，支持工具调用"""
#     # 默认工具集（可扩展）
#     tools = tools or [get_filenames_in_directory, get_file_content, delete_file, create_file]  # 按需添加其他工具
    
#     # 构建系统提示（包含 RAG 上下文）
#     vectorstore = Chroma(embedding_function=embedder, persist_directory="./chroma_db")
#     retriever = vectorstore.as_retriever()
#     docs = retriever.invoke(question)
#     context = "\n\n".join(doc.page_content for doc in docs)
    
#     system_prompt = f"""你是一个基于检索增强生成（RAG）的助手。
#     以下是检索到的上下文信息：
#     {context}
    
#     你可以根据用户的问题选择以下方式回答：
#     1. 直接使用上下文信息回答（若内容足够）。
#     2. 调用工具进行操作。
#     """
    
#     # 调用基础聊天机器人（支持工具）
#     return chatbot_answer(
#         question=question,
#         tools=tools,
#         system_prompt=system_prompt
#     )