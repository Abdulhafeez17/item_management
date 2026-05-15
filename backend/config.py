import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")

load_dotenv(f".env.{ENV}")

class Config:
    ENV = ENV
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DEBUG = os.getenv("DEBUG") == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL")