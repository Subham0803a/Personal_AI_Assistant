from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, query, documents
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal AI Knowledge Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router,    prefix="/api", tags=["upload"])
app.include_router(query.router,     prefix="/api", tags=["query"])
app.include_router(documents.router, prefix="/api", tags=["documents"])

@app.get("/health")
async def health():
    return {"status": "ok"}