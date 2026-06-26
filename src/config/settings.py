import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]

APP_ENV = os.getenv(
    "APP_ENV",
    "dev"
).lower()

CONFIG_FILE = (
    ROOT_DIR
    / "config"
    / f"{APP_ENV}.env"
)

ROOT_ENV_FILE = (
    ROOT_DIR
    / ".env"
)


if CONFIG_FILE.exists():
    load_dotenv(
        CONFIG_FILE,
        override=False
    )


if ROOT_ENV_FILE.exists():
    load_dotenv(
        ROOT_ENV_FILE,
        override=False
    )


APP_NAME = os.getenv(
    "APP_NAME",
    "RecruitVerse"
)

DEBUG = os.getenv(
    "DEBUG",
    "false"
).lower() == "true"

API_VERSION = os.getenv(
    "API_VERSION",
    "v1"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

RATE_LIMIT = os.getenv(
    "RATE_LIMIT",
    "20/minute"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "recruiters"
)

DB_USER = os.getenv(
    "DB_USER",
    "postgres"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    ""
)

DB_HOST = os.getenv(
    "DB_HOST",
    "127.0.0.1"
)

DB_PORT = os.getenv(
    "DB_PORT",
    "5433"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret"
)


def get_database_config():

    return {
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT
    }


def get_database_url():

    return (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def settings_summary():

    return {
        "app_name": APP_NAME,
        "app_env": APP_ENV,
        "debug": DEBUG,
        "api_version": API_VERSION,
        "log_level": LOG_LEVEL,
        "rate_limit": RATE_LIMIT,
        "db_name": DB_NAME,
        "db_user": DB_USER,
        "db_host": DB_HOST,
        "db_port": DB_PORT
    }