import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config.settings import (
    LOG_LEVEL
)


ROOT_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = (
    ROOT_DIR
    / "logs"
)

LOG_FILE = (
    LOG_DIR
    / "app.log"
)


def get_logger(
        name="recruitverse"):

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(
        name
    )

    if logger.handlers:
        return logger

    level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO
    )

    logger.setLevel(
        level
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

    return logger


logger = get_logger()