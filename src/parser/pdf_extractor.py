from pathlib import Path

import fitz

from src.utils.logger import (
    logger
)


OUTPUT_FOLDER = Path(
    "data/parsed_resumes/raw_text"
)


def ensure_output_folder():

    if OUTPUT_FOLDER.exists() and not OUTPUT_FOLDER.is_dir():

        backup_path = OUTPUT_FOLDER.with_name(
            OUTPUT_FOLDER.name + "_backup.txt"
        )

        OUTPUT_FOLDER.rename(
            backup_path
        )

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


def extract_text(
        pdf_path):

    try:
        pdf_path = Path(
            pdf_path
        )

        if not pdf_path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        text_parts = []

        with fitz.open(
                pdf_path
        ) as document:

            for page in document:

                text_parts.append(
                    page.get_text()
                )

        return "\n".join(
            text_parts
        ).strip()

    except Exception as error:

        logger.error(
            f"Resume text extraction failed: {error}"
        )

        raise


def safe_extract_text(
        pdf_path):

    try:
        return extract_text(
            pdf_path
        )

    except Exception as error:

        logger.error(
            f"Safe extraction failed: {error}"
        )

        return ""


def save_extracted_text(
        pdf_path,
        output_folder=OUTPUT_FOLDER):

    ensure_output_folder()

    text = extract_text(
        pdf_path
    )

    output_path = Path(
        output_folder
    ) / f"{Path(pdf_path).stem}.txt"

    output_path.write_text(
        text,
        encoding="utf-8"
    )

    return output_path


if __name__ == "__main__":

    ensure_output_folder()