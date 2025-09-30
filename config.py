from dotenv import load_dotenv
import os

load_dotenv()

telegram_token=os.getenv("TELEGRAM_TOKEN")

if not telegram_token:
    raise ValueError("No telegram_token found in .env")
