from celery import Celery
from app.config import get_settings
from app.services.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_and_store
from app.database import SessionLocal
from app.models.document import Document

settings = get_settings()
celery_app = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task(name="ingest_document")
def ingest_document(doc_id: str, file_path: str):
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        doc.status = "processing"
        db.commit()

        text   = extract_text(file_path)
        chunks = chunk_text(text, doc_id)
        embed_and_store(chunks)

        doc.status      = "ready"
        doc.chunk_count = len(chunks)
        db.commit()
    except Exception as e:
        doc.status = "error"
        doc.error  = str(e)
        db.commit()
        raise
    finally:
        db.close()