from src.utils.logger import (
    LOG_FILE,
    logger
)


def test_logger_writes_file():

    logger.info(
        "Resume Uploaded"
    )

    for handler in logger.handlers:
        handler.flush()

    assert LOG_FILE.exists()

    content = LOG_FILE.read_text(
        encoding="utf-8"
    )

    assert "Resume Uploaded" in content