from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_PREFIX = os.getenv("BOT_PREFIX")
    MONGO_DB_TOKEN = os.getenv("MONGO_DB_TOKEN")

settings = Settings()