from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start, handle_message, handle_document
from bot.config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()