import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def default_db_uri():
    db_path = (Path(__file__).resolve().parent.parent / "instance" / "app.db").resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_path.as_posix()}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", default_db_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
