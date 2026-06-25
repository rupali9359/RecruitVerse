def normalize_skills(
        skills):

    if not skills:

        return set()

    return {
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    }


def recommend_role(
        skills):

    skill_set = normalize_skills(
        skills
    )

    if (
            "machine learning" in skill_set
            or "deep learning" in skill_set
            or "nlp" in skill_set
    ) and (
            "python" in skill_set
            or "sql" in skill_set
    ):

        return "Data Scientist"

    if (
            "power bi" in skill_set
            or "tableau" in skill_set
            or "excel" in skill_set
    ) and (
            "sql" in skill_set
            or "python" in skill_set
    ):

        return "Data Analyst"

    if (
            "fastapi" in skill_set
            or "django" in skill_set
            or "flask" in skill_set
    ) and (
            "python" in skill_set
    ):

        return "Backend Developer"

    if (
            "docker" in skill_set
            or "kubernetes" in skill_set
            or "aws" in skill_set
    ):

        return "DevOps Engineer"

    if (
            "streamlit" in skill_set
            or "plotly" in skill_set
            or "pandas" in skill_set
    ):

        return "Data App Developer"

    return "General IT Role"