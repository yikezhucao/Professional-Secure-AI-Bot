import os

from langchain_ollama.chat_models import ChatOllama

# Establishes one central place for the LLM, to make it adjustable


def get_llm() -> ChatOllama:
    """Returns the LLM, this allows for a central place to change the LLM to other providers or local."""
    llm = ChatOllama(
        model="llama3.2:latest",
        # model="deepseek-r1:32b",
        # model="qwen2.5:32b",
        # model="qwen2.5:3b",
        base_url="http://192.168.22.234:11434"
        )
    return llm
