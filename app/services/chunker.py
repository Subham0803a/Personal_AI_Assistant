from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

CHUNK_SIZE    = 500   # tokens
CHUNK_OVERLAP = 50

def _token_len(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def chunk_text(text: str, doc_id: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=_token_len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    raw_chunks = splitter.split_text(text)
    return [
        {
            "id":          f"{doc_id}-{i}",
            "doc_id":      doc_id,
            "chunk_index": i,
            "content":     chunk,
            "token_count": _token_len(chunk),
        }
        for i, chunk in enumerate(raw_chunks)
    ]