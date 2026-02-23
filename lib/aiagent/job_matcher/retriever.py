# retriever.py
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="nomic-embed-text")
persist_dir="chroma_json_db"
add_documents = not os.path.exists(persist_dir)

def build_retriever(data):
    if add_documents:
        documents = []
        ids = []

        for i, job in enumerate(data):
            tools = ", ".join(job.get("tools_requirement", []))
            responsibilities = "\n".join(job.get("responsibilities", []))

            content = f"""
            Title: {job.get("title", "")}
            Company: {job.get("company_name", "")}
            Location: {job.get("location", "")}
            Years of Experience: {job.get("years_of_experience","")}

            Description:
            {job.get("description", "")}
            
            Responsibilities:
            {responsibilities}

            Tools:
            {tools}
            """

            document = Document(
                page_content=content.strip(),
                metadata={
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "schedule_type": job.get("schedule_type"),
                    "ingestion_date": job.get("ingestion_date"),
                    "job_url": job.get("job_url"),
                },
                id=str(i)
            )

            documents.append(document)
            ids.append(str(i))
        
    vector_store = Chroma(
        collection_name="job_postings",
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    
    if add_documents:
        vector_store.add_documents(documents=documents, ids=ids)

    retriever = vector_store.as_retriever(
        search_type="mmr",   
        search_kwargs={
            "k": 12,         
            "fetch_k": 20
        }
    )

    return retriever