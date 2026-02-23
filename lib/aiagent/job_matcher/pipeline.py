# pipeline.py
from langchain_ollama.llms import OllamaLLM
from .retriever import build_retriever
from .prompt_builder import format_context, build_prompt

model = OllamaLLM(model="ministral-3")

def run_agent(cv_text,data):

    retriever = build_retriever(data)

    # 1. Retrieve
    retrieved_docs = retriever.invoke(cv_text)

    # 3. Format context
    context = format_context(retrieved_docs)

    # 4. Build final prompt
    prompt = build_prompt(cv_text, context)

    # 5. Generate
    result = model.invoke(prompt)

    return result