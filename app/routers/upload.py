from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil, uuid
from app.database import get_db
from app.models.document import Document
from app.worker import ingest_document
from app.config import get_settings

router   = APIRouter()
settings = get_settings()

ALLOWED_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only PDF, TXT, DOCX allowed")

    doc_id     = str(uuid.uuid4())
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_name = f"{doc_id}_{file.filename}"
    file_path = upload_dir / safe_name

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc = Document(
        id=doc_id,
        filename=safe_name,
        original_name=file.filename,
        file_path=str(file_path),
        status="pending",
    )
    db.add(doc)
    db.commit()

    ingest_document.delay(doc_id, str(file_path))

    return {"document_id": doc_id, "filename": file.filename, "status": "pending"}