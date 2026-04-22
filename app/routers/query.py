from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import get_rag_chain
from app.observability.tracer import get_callbacks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/query", response_model=QueryResponse)
async def query_knowledge(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")

    chain     = get_rag_chain(top_k=req.top_k)
    callbacks = get_callbacks()

    result = chain.invoke(
        {"query": req.question},
        config={"callbacks": callbacks},
    )

    sources = list({
        doc.metadata.get("doc_id", "unknown")
        for doc in result.get("source_documents", [])
    })

    return QueryResponse(answer=result["result"], sources=sources)