from src.matching.skill_extractor import (
    extract_skills
)

from src.matching.matching_engine import (
    calculate_match_score
)


def test_skill_extraction():

    skills = [
        "Python",
        "SQL",
        "Machine Learning"
    ]

    text = """
    Python SQL
    """

    result = extract_skills(
        text,
        skills
    )

    assert "Python" in result

    assert "SQL" in result


def test_match_score():

    resume = [
        "Python",
        "SQL"
    ]

    jd = [
        "Python",
        "SQL",
        "AWS"
    ]

    score, matched = calculate_match_score(
        resume,
        jd
    )

    assert score == 66.67

    assert "Python" in matched

    assert "SQL" in matched

    assert "AWS" not in matched