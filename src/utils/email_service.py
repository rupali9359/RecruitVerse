import os
from pathlib import Path

from dotenv import load_dotenv

from src.utils.logger import (
    logger
)


ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(
    ROOT_DIR / ".env"
)


try:
    import yagmail
except ImportError:
    yagmail = None


def send_email(
        receiver,
        subject,
        message):

    dry_run = os.getenv(
        "EMAIL_DRY_RUN",
        "true"
    ).lower() == "true"

    sender_email = os.getenv(
        "SMTP_EMAIL"
    )

    app_password = os.getenv(
        "SMTP_APP_PASSWORD"
    )

    if dry_run:

        logger.info(
            f"Email dry run to {receiver}: {subject} - {message}"
        )

        return {
            "success": True,
            "message": "Email dry run successful"
        }

    if not sender_email or not app_password:

        logger.error(
            "Email credentials are missing"
        )

        return {
            "success": False,
            "message": "Email credentials are missing"
        }

    if yagmail is None:

        logger.error(
            "yagmail is not installed"
        )

        return {
            "success": False,
            "message": "yagmail is not installed"
        }

    try:

        yag = yagmail.SMTP(
            sender_email,
            app_password
        )

        yag.send(
            to=receiver,
            subject=subject,
            contents=message
        )

        logger.info(
            f"Email sent to {receiver}: {subject}"
        )

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as error:

        logger.error(
            f"Email sending failed: {error}"
        )

        return {
            "success": False,
            "message": str(
                error
            )
        }