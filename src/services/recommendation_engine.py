def generate_recommendation(
        final_score,
        missing_skills):

    if final_score >= 85:

        return (
            "Strong Candidate. "
            "Recommend Interview."
        )

    if len(
            missing_skills
    ) <= 2:

        return (
            "Good Candidate. "
            "Requires Skill Improvement."
        )

    return (
        "Weak Match. "
        "Candidate needs significant upskilling."
    )