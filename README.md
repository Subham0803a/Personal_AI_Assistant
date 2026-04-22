# Personal AI Knowledge Assistant

Upload PDFs, DOCX, and TXT files. Ask questions. Get answers grounded in your own documents.

## Stack
- **FastAPI** — REST API
- **LangChain + ChromaDB** — RAG pipeline
- **OpenAI** — embeddings + GPT-4o-mini
- **Celery + Redis** — async ingestion
- **PostgreSQL** — metadata store
- **Telegram bot** — chat interface
- **React + Vite** — web dashboard
- **MCP server** — agent-callable tools

## Quick start
\`\`\`bash
cp .env.example .env        # fill in your keys
docker-compose up -d        # starts all services
\`\`\`

API runs at http://localhost:8000  
Dashboard at http://localhost:3000

## Build order
1. FastAPI + file upload
2. PDF parsing + chunking
3. Embed + store in ChromaDB
4. RAG retrieval chain
5. Prompt engineering
6. Telegram interface
7. MCP server
8. LLMOps + monitoring
9. Docker deploy