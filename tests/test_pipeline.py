from pathlib import Path

import fitz

from src.services.resume_pipeline import (
    process_resume
)


def test_pipeline():

    resume_pdf_path = Path(
        "tests/pipeline_resume.pdf"
    )

    job_description_path = Path(
        "tests/pipeline_job_description.txt"
    )

    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (
            72,
            72
        ),
        "Python SQL Machine Learning"
    )

    document.save(
        resume_pdf_path
    )

    document.close()

    job_description_path.write_text(
        "Python SQL AWS",
        encoding="utf-8"
    )

    result = process_resume(
        resume_pdf_path,
        job_description_path
    )

    assert result[
        "keyword_score"
    ] >= 0

    assert "Python" in result[
        "matched_skills"
    ]

    assert "SQL" in result[
        "matched_skills"
    ]