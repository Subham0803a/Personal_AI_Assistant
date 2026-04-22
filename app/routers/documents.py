from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.services.vectorstore import delete_document_vectors

router = APIRouter()

@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.created_at.desc()).all()
    return [
        {"id": d.id, "filename": d.original_name,
         "status": d.status, "chunk_count": d.chunk_count, "created_at": d.created_at}
        for d in docs
    ]

@router.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(404, "Document not found")
    delete_document_vectors(doc_id)
    db.delete(doc)
    db.commit()
    return {"deleted": doc_id}