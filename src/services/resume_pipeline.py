from pathlib import Path

from src.matching.matching_engine import (
    calculate_match_score
)

from src.matching.skill_extractor import (
    extract_skills
)

from src.parser.pdf_extractor import (
    extract_text
)

from src.utils.logger import (
    logger
)

from src.utils.validation import (
    validate_pdf_file
)


DEFAULT_SKILLS = [
    "Python",
    "SQL",
    "Machine Learning",
    "AWS",
    "Docker",
    "FastAPI",
    "PostgreSQL",
    "Streamlit",
    "Pandas"
]


def process_resume(
        resume_pdf_path,
        job_description_path,
        skills=None):

    try:
        validate_pdf_file(
            resume_pdf_path
        )

        resume_text = extract_text(
            resume_pdf_path
        )

        job_description_text = Path(
            job_description_path
        ).read_text(
            encoding="utf-8"
        )

        skills = skills or DEFAULT_SKILLS

        resume_skills = extract_skills(
            resume_text,
            skills
        )

        job_skills = extract_skills(
            job_description_text,
            skills
        )

        keyword_score, matched_skills = calculate_match_score(
            resume_skills,
            job_skills
        )

        result = {
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": matched_skills,
            "keyword_score": keyword_score
        }

        logger.info(
            f"Resume processed successfully: {result}"
        )

        return result

    except Exception as error:

        logger.error(
            f"Resume pipeline failed: {error}"
        )

        raise