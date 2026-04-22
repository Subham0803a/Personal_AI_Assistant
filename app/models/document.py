from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Document(Base):
    __tablename__ = "documents"
    
    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename     = Column(String, nullable=False)
    original_name= Column(String, nullable=False)
    file_path    = Column(String, nullable=False)
    status       = Column(String, default="pending")   # pending|processing|ready|error
    chunk_count  = Column(Integer, default=0)
    error        = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())