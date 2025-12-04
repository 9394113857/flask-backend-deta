import os
from datetime import timedelta
from dotenv import load_dotenv

# Load local .env only (Railway ignores this)
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    PROPAGATE_EXCEPTIONS = True
