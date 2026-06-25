def clean_skills(
        skills):

    if not skills:

        return []

    return [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]


def identify_strengths(
        matched_skills):

    return clean_skills(
        matched_skills
    )


def identify_weaknesses(
        missing_skills):

    return clean_skills(
        missing_skills
    )


def skill_gap_percentage(
        matched,
        required):

    if isinstance(
            matched,
            list
    ):

        matched_count = len(
            matched
        )

    else:

        matched_count = int(
            matched
        )

    if isinstance(
            required,
            list
    ):

        required_count = len(
            required
        )

    else:

        required_count = int(
            required
        )

    if required_count <= 0:

        return 0

    gap = max(
        required_count - matched_count,
        0
    )

    return round(
        (
            gap / required_count
        ) * 100,
        2
    )


def generate_strength_summary(
        matched_skills):

    strengths = identify_strengths(
        matched_skills
    )

    if not strengths:

        return (
            "No major strengths identified from the matched skills."
        )

    return (
        "Candidate strengths include: "
        + ", ".join(
            strengths
        )
        + "."
    )


def generate_weakness_summary(
        missing_skills):

    weaknesses = identify_weaknesses(
        missing_skills
    )

    if not weaknesses:

        return (
            "No major skill weaknesses identified."
        )

    return (
        "Candidate needs improvement in: "
        + ", ".join(
            weaknesses
        )
        + "."
    )