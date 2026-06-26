from src.ml_model.predict_score import (
    predict_candidate_score
)

from pathlib import Path


def calculate_resume_score(
        keyword_score,
        semantic_score,
        matched,
        jd_skills):

    final_score = predict_candidate_score(
        keyword_score,
        semantic_score,
        len(matched),
        len(jd_skills)
    )

    return final_score


def _read_text_from_file(
        file_path):

    file_path = Path(
        file_path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() == ".pdf":

        try:
            import fitz

            text_parts = []

            with fitz.open(
                    file_path
            ) as document:

                for page in document:

                    text_parts.append(
                        page.get_text()
                    )

            return "\n".join(
                text_parts
            )

        except Exception:

            return ""

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def _extract_basic_skills(
        text):

    known_skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "nlp",
        "pandas",
        "numpy",
        "scikit-learn",
        "fastapi",
        "streamlit",
        "postgresql",
        "docker",
        "git",
        "javascript",
        "react",
        "html",
        "css",
        "aws",
        "data science",
        "data analysis"
    ]

    text = (
        text or ""
    ).lower()

    matched_skills = [
        skill
        for skill in known_skills
        if skill in text
    ]

    return matched_skills


def calculate_resume_score(
        keyword_score,
        semantic_score,
        matched,
        jd_skills):

    try:
        from src.ml_model.predict_score import (
            predict_candidate_score
        )

        return predict_candidate_score(
            keyword_score,
            semantic_score,
            len(matched),
            len(jd_skills)
        )

    except Exception:

        return round(
            (
                keyword_score * 0.4
            ) + (
                semantic_score * 0.6
            ),
            2
        )


def process_resume(
        resume_path,
        job_description_path=None,
        job_description_text=None):

    resume_text = _read_text_from_file(
        resume_path
    )

    if job_description_text:

        jd_text = job_description_text

    elif job_description_path:

        job_description_path = Path(
            job_description_path
        )

        if job_description_path.exists():

            jd_text = _read_text_from_file(
                job_description_path
            )

        else:

            jd_text = str(
                job_description_path
            )

    else:

        jd_text = ""

    resume_skills = _extract_basic_skills(
        resume_text
    )

    jd_skills = _extract_basic_skills(
        jd_text
    )

    matched = sorted(
        set(
            resume_skills
        ).intersection(
            set(
                jd_skills
            )
        )
    )

    if jd_skills:

        keyword_score = round(
            (
                len(
                    matched
                ) / len(
                    jd_skills
                )
            ) * 100,
            2
        )

    else:

        keyword_score = 0.0

    semantic_score = keyword_score

    final_score = calculate_resume_score(
        keyword_score,
        semantic_score,
        matched,
        jd_skills
    )

    return {
        "resume_path": str(
            resume_path
        ),
        "matched": matched,
        "matched_skills": matched,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "score": final_score,
        "final_score": final_score
    }

from pathlib import Path


def _read_pipeline_text(
        source):

    source_path = Path(
        str(
            source
        )
    )

    if source_path.exists():

        if source_path.suffix.lower() == ".pdf":

            try:
                import fitz

                text_parts = []

                with fitz.open(
                        source_path
                ) as document:

                    for page in document:

                        text_parts.append(
                            page.get_text()
                        )

                return "\n".join(
                    text_parts
                )

            except Exception:

                return ""

        return source_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    return str(
        source
    )


def _extract_pipeline_skills(
        text):

    skill_map = {
        "python": "Python",
        "sql": "SQL",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "nlp": "NLP",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",
        "fastapi": "FastAPI",
        "streamlit": "Streamlit",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "docker": "Docker",
        "git": "Git",
        "javascript": "JavaScript",
        "react": "React",
        "html": "HTML",
        "css": "CSS",
        "aws": "AWS",
        "data science": "Data Science",
        "data analysis": "Data Analysis"
    }

    text = (
        text or ""
    ).lower()

    matched_skills = []

    for keyword, display_name in skill_map.items():

        if keyword in text and display_name not in matched_skills:

            matched_skills.append(
                display_name
            )

    return matched_skills


def process_resume(
        resume_path,
        job_description_path=None,
        job_description_text=None):

    resume_text = _read_pipeline_text(
        resume_path
    )

    resume_skills = _extract_pipeline_skills(
        resume_text
    )

    if job_description_text:

        jd_text = job_description_text

    elif job_description_path:

        jd_text = _read_pipeline_text(
            job_description_path
        )

    else:

        jd_text = ""

    if jd_text:

        jd_skills = _extract_pipeline_skills(
            jd_text
        )

        matched = [
            skill
            for skill in resume_skills
            if skill in jd_skills
        ]

        return matched

    return resume_skills

from pathlib import Path


def _read_pipeline_text(
        source):

    source_path = Path(
        str(
            source
        )
    )

    if source_path.exists():

        if source_path.suffix.lower() == ".pdf":

            try:
                import fitz

                text_parts = []

                with fitz.open(
                        source_path
                ) as document:

                    for page in document:

                        text_parts.append(
                            page.get_text()
                        )

                return "\n".join(
                    text_parts
                )

            except Exception:

                return ""

        return source_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    return str(
        source
    )


def _extract_pipeline_skills(
        text):

    skill_map = {
        "python": "Python",
        "sql": "SQL",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "nlp": "NLP",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",
        "fastapi": "FastAPI",
        "streamlit": "Streamlit",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "docker": "Docker",
        "git": "Git",
        "javascript": "JavaScript",
        "react": "React",
        "html": "HTML",
        "css": "CSS",
        "aws": "AWS",
        "data science": "Data Science",
        "data analysis": "Data Analysis"
    }

    text = (
        text or ""
    ).lower()

    matched_skills = []

    for keyword, display_name in skill_map.items():

        if keyword in text and display_name not in matched_skills:

            matched_skills.append(
                display_name
            )

    return matched_skills


def calculate_resume_score(
        keyword_score,
        semantic_score,
        matched,
        jd_skills):

    try:
        from src.ml_model.predict_score import (
            predict_candidate_score
        )

        return predict_candidate_score(
            keyword_score,
            semantic_score,
            len(matched),
            len(jd_skills)
        )

    except Exception:

        return round(
            (
                keyword_score * 0.4
            ) + (
                semantic_score * 0.6
            ),
            2
        )


def process_resume(
        resume_path,
        job_description_path=None,
        job_description_text=None):

    resume_text = _read_pipeline_text(
        resume_path
    )

    resume_skills = _extract_pipeline_skills(
        resume_text
    )

    if job_description_text:

        jd_text = job_description_text

    elif job_description_path:

        jd_text = _read_pipeline_text(
            job_description_path
        )

    else:

        jd_text = ""

    jd_skills = _extract_pipeline_skills(
        jd_text
    )

    if jd_skills:

        matched_skills = [
            skill
            for skill in resume_skills
            if skill in jd_skills
        ]

        keyword_score = round(
            (
                len(
                    matched_skills
                ) / len(
                    jd_skills
                )
            ) * 100,
            2
        )

    else:

        matched_skills = resume_skills
        keyword_score = 0.0

    semantic_score = keyword_score

    final_score = calculate_resume_score(
        keyword_score,
        semantic_score,
        matched_skills,
        jd_skills
    )

    return {
        "resume_path": str(
            resume_path
        ),
        "resume_text": resume_text,
        "job_description": jd_text,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "matched": matched_skills,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "score": final_score,
        "final_score": final_score
    }