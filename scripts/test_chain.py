from app.services.rag_chain import get_rag_chain

QUESTIONS = [
    "What documents have been uploaded?",
    "Summarise the key points in my knowledge base.",
]

if __name__ == "__main__":
    chain = get_rag_chain()
    for q in QUESTIONS:
        print(f"Q: {q}")
        result = chain.invoke({"query": q})
        print(f"A: {result['result']}")
        print(f"   Sources: {[d.metadata.get('doc_id') for d in result['source_documents']]}\n")