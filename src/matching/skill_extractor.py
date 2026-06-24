def extract_skills(
        text,
        skills):

    found_skills = []

    text_lower = text.lower()

    for skill in skills:

        if skill.lower() in text_lower:

            found_skills.append(
                skill
            )

    return found_skills