from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from app.services.vectorstore import get_vectorstore
from app.prompts.rag_prompt import rag_prompt
from app.config import get_settings
from functools import lru_cache

settings = get_settings()

@lru_cache(maxsize=1)
def get_rag_chain(top_k: int = 5):
    vectorstore = get_vectorstore()
    retriever   = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=settings.openai_api_key,
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": rag_prompt},
    )