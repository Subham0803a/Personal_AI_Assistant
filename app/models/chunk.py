from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.database import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id          = Column(String, primary_key=True)
    doc_id      = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content     = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)