def clean_skills(
        skills):

    if not skills:

        return []

    return [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]


def generate_summary(
        skills,
        recommended_role=None):

    skills = clean_skills(
        skills
    )

    if not skills:

        return (
            "Candidate summary: "
            "Candidate profile has limited skill information."
        )

    skill_text = ", ".join(
        skills
    )

    if recommended_role:

        return (
            f"Candidate demonstrates skills in {skill_text}. "
            f"Profile is suitable for {recommended_role} roles."
        )

    return (
        f"Candidate demonstrates skills in {skill_text}. "
        "Profile is suitable for technology and data-driven roles."
    )