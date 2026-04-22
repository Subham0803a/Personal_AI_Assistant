from langchain_openai import OpenAIEmbeddings
import chromadb
from app.config import get_settings

settings = get_settings()

_client     = chromadb.PersistentClient(path=settings.chroma_path)
_collection = _client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"},
)
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.openai_api_key,
)

def embed_and_store(chunks: list[dict]):
    if not chunks:
        return
    texts     = [c["content"]     for c in chunks]
    ids       = [c["id"]          for c in chunks]
    metadatas = [{"doc_id": c["doc_id"], "chunk_index": c["chunk_index"]} for c in chunks]

    BATCH = 100
    for i in range(0, len(texts), BATCH):
        vectors = embedder.embed_documents(texts[i:i+BATCH])
        _collection.upsert(
            ids=ids[i:i+BATCH],
            embeddings=vectors,
            documents=texts[i:i+BATCH],
            metadatas=metadatas[i:i+BATCH],
        )