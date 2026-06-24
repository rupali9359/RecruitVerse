import pytest

from src.utils.validation import (
    validate_pdf_file
)


def test_validate_pdf_file_accepts_pdf():

    assert validate_pdf_file(
        "resume.pdf"
    )


def test_validate_pdf_file_rejects_txt():

    with pytest.raises(
        ValueError
    ):

        validate_pdf_file(
            "resume.txt"
        )