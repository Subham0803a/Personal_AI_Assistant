from pathlib import Path
from unstructured.partition.auto import partition

def extract_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    elements = partition(filename=str(path))

    # Filter very short fragments like page numbers / headers
    chunks = [str(el) for el in elements if len(str(el).strip()) > 30]
    return "\n\n".join(chunks)