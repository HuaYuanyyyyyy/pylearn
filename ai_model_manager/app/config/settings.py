from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AI Model Manager")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False") == "True"

DATABASE_URL = os.getenv("DATABASE_URL")