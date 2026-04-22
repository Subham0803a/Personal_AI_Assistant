import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL:   str = os.getenv("API_URL", "http://localhost:8000")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env")