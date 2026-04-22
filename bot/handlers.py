from telegram import Update
from telegram.ext import ContextTypes
import httpx
from bot.config import API_URL

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm your personal AI assistant.\n\n"
        "• Send a message to ask a question\n"
        "• Send a PDF / TXT / DOCX to add it to your knowledge base\n"
    )

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    if not question:
        return
    thinking = await update.message.reply_text("Thinking…")
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(
                f"{API_URL}/api/query",
                json={"question": question, "top_k": 5},
            )
            data   = resp.json()
            answer = data["answer"]
            if data.get("sources"):
                answer += f"\n\n📎 Sources: {', '.join(data['sources'])}"
        except Exception as e:
            answer = f"Error: {e}"
    await thinking.edit_text(answer)

async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc  = update.message.document
    await update.message.reply_text(f"Uploading {doc.file_name}…")
    file    = await ctx.bot.get_file(doc.file_id)
    content = await file.download_as_bytearray()
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{API_URL}/api/upload",
            files={"file": (doc.file_name, bytes(content), doc.mime_type)},
        )
        data = resp.json()
    await update.message.reply_text(
        f"✅ {doc.file_name} uploaded! Processing in background…\n"
        f"ID: {data['document_id']}"
    )