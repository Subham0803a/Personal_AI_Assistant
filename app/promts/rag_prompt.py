from langchain_core.prompts import PromptTemplate

_TEMPLATE = """You are a helpful assistant. Answer using ONLY the context below.
If the answer is not in the context, say exactly:
"I don't have that information in your documents."

Context:
{context}

Question: {question}

Rules:
- Cite sources inline as [doc: <doc_id>].
- Be concise. Use bullet points for lists.
- Never make up information.

Answer:"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=_TEMPLATE,
)