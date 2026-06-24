def calculate_match_score(
        resume_skills,
        job_skills):

    if not job_skills:

        return 0, []

    matched_skills = []

    resume_skills_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    for skill in job_skills:

        if skill.lower() in resume_skills_lower:

            matched_skills.append(
                skill
            )

    score = (
        len(matched_skills)
        / len(job_skills)
    ) * 100

    return round(
        score,
        2
    ), matched_skills