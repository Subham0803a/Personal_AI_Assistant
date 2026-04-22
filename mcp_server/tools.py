from mcp.types import Tool, TextContent
import httpx

API_URL = "http://localhost:8000"

async def list_tools_handler():
    return [
        Tool(
            name="query_knowledge_base",
            description="Ask a question and get an answer from the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "top_k":    {"type": "integer", "default": 5},
                },
                "required": ["question"],
            },
        ),
        Tool(
            name="list_documents",
            description="List all documents indexed in the knowledge base",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="ingest_file_url",
            description="Download a file from a URL and ingest it",
            inputSchema={
                "type": "object",
                "properties": {
                    "url":      {"type": "string"},
                    "filename": {"type": "string"},
                },
                "required": ["url", "filename"],
            },
        ),
    ]

async def call_tool_handler(name: str, arguments: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        if name == "query_knowledge_base":
            r    = await client.post(f"{API_URL}/api/query", json=arguments)
            data = r.json()
            return [TextContent(type="text", text=data["answer"])]

        elif name == "list_documents":
            r    = await client.get(f"{API_URL}/api/documents")
            docs = r.json()
            lines = [
                f"- {d['filename']} ({d['status']}, {d['chunk_count']} chunks)"
                for d in docs
            ]
            return [TextContent(type="text", text="\n".join(lines) or "No documents.")]

        elif name == "ingest_file_url":
            async with httpx.AsyncClient() as dl:
                file_resp = await dl.get(arguments["url"])
            r    = await client.post(
                f"{API_URL}/api/upload",
                files={"file": (arguments["filename"], file_resp.content)},
            )
            data = r.json()
            return [TextContent(type="text", text=f"Ingested: {data['document_id']}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]