import os

from langchain_ollama.chat_models import ChatOllama

# Establishes one central place for the LLM, to make it adjustable


def get_llm() -> ChatOllama:
    """Returns the LLM, this allows for a central place to change the LLM to other providers or local."""
    llm = ChatOllama(
        model="llama3.2",
        base_url="http://192.168.22.234:11434"
        )
    return llm
