from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.agents import create_tool_calling_agent, AgentExecutor

from professional_secure_ai_bot.ai_tools.ai_llm import get_llm
from professional_secure_ai_bot.ai_tools.embedder import get_embedder
from professional_secure_ai_bot.tools.file_management import (
    get_filenames_in_directory,
    get_file_content,
    delete_file,
    create_file,
    execute_linux_command
)
from professional_secure_ai_bot.tools.web_content import get_web_content
from operator import itemgetter


# 初始化 LLM 和 Embedder
llm = get_llm()
embedder = get_embedder()

# 定义工具列表
tools = [
    get_filenames_in_directory,
    get_file_content,
    delete_file,
    create_file,
    get_web_content,
    execute_linux_command,
]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# 自定义 Prompt Template（添加必要的 agent 字段）
prompt = PromptTemplate.from_template(
    """You are a helpful assistant that answers questions by retrieving information from documents and calling external tools when necessary.

    Instructions:
    - First, check the provided context for the answer.
    - If the answer isn't found, use one of the available tools to retrieve it.
    - Always respond in natural language, never output code or internal variables.
    
    Available tools: {tool_names}
    Tool descriptions: {tools}
    
    Question: {input}
    Context: {context}
    
    {agent_scratchpad}
    
    Final Answer:
    """
)

# prompt = PromptTemplate.from_template(
#      """Answer the following question: {input} using the context provided below.
#     If the answer is not in the context, say "Sorry, I don't know."

#     You have access to the following tools: {tool_names}

#     {tools}

#     Question: {input}

#     Context: {context}

#     {agent_scratchpad}

#     Answer:
#     """
# )

# 创建支持工具调用的 Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def rag_answer(question: str) -> str:
    """Uses the base_chatbot.py to implement a chatbot that can access a vectorstore and external tools."""
    
    # 构建向量数据库检索器
    vectorstore = Chroma(embedding_function=embedder, persist_directory="./chroma_db")
    retriever = vectorstore.as_retriever()

    #构建完整的 RAG Chain 并整合 Agent Executor
    def _prepare_input(question: str):
        return {
            "input": question,
            "context": format_docs(retriever.invoke(question)),
            "tool_names": [tool.name for tool in tools],
            "tools": "\n".join([tool.description for tool in tools]),
        }
    def extract_full_result(result):
        return {
            "answer": result["output"],
            "intermediate_steps": result.get("intermediate_steps", []),
            "log": "\n".join([
                f"Step {i+1}: {step[0].tool} with {step[0].tool_input}\nOutput: {step[1]}"
                for i, step in enumerate(result.get("intermediate_steps", []))
            ])
        }
    
    rag_chain = (
        RunnablePassthrough()
        | _prepare_input
        | agent_executor
        | extract_full_result
    )

    return rag_chain.invoke(question)