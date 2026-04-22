import chromadb
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import get_settings

settings = get_settings()

def get_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.openai_api_key,
    )
    return Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=embeddings,
        collection_name="knowledge_base",
    )

def delete_document_vectors(doc_id: str):
    client  = chromadb.PersistentClient(path=settings.chroma_path)
    col     = client.get_collection("knowledge_base")
    results = col.get(where={"doc_id": doc_id})
    if results["ids"]:
        col.delete(ids=results["ids"])