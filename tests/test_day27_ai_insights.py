from src.ai_insights.candidate_analyzer import (
    identify_strengths,
    identify_weaknesses,
    skill_gap_percentage
)

from src.ai_insights.insight_engine import (
    generate_summary
)

from src.ai_insights.recruiter_copilot import (
    generate_insights
)

from src.ai_insights.role_recommender import (
    recommend_role
)


def test_generate_summary():

    summary = generate_summary(
        [
            "Python",
            "SQL",
            "Machine Learning"
        ],
        "Data Scientist"
    )

    assert "Python" in summary

    assert "Data Scientist" in summary


def test_strength_analysis():

    strengths = identify_strengths(
        [
            "Python",
            "SQL"
        ]
    )

    assert "Python" in strengths

    assert "SQL" in strengths


def test_weakness_analysis():

    weaknesses = identify_weaknesses(
        [
            "AWS",
            "Tableau"
        ]
    )

    assert "AWS" in weaknesses

    assert "Tableau" in weaknesses


def test_skill_gap_percentage():

    gap = skill_gap_percentage(
        8,
        10
    )

    assert gap == 20.0


def test_role_recommendation():

    role = recommend_role(
        [
            "Python",
            "SQL",
            "Machine Learning"
        ]
    )

    assert role == "Data Scientist"


def test_generate_insights():

    insights = generate_insights(
        [
            "Python",
            "SQL",
            "Machine Learning"
        ],
        [
            "AWS",
            "Tableau"
        ],
        [
            "Python",
            "SQL",
            "Machine Learning",
            "AWS",
            "Tableau"
        ],
        86
    )

    assert insights[
        "recommended_role"
    ] == "Data Scientist"

    assert insights[
        "skill_gap_percentage"
    ] == 40.0

    assert "Python" in insights[
        "strengths"
    ]

    assert "AWS" in insights[
        "weaknesses"
    ]

    assert "summary" in insights