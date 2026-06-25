from src.ai_insights.candidate_analyzer import (
    generate_strength_summary,
    generate_weakness_summary,
    identify_strengths,
    identify_weaknesses,
    skill_gap_percentage
)

from src.ai_insights.insight_engine import (
    generate_summary
)

from src.ai_insights.role_recommender import (
    recommend_role
)


def generate_insights(
        matched_skills,
        missing_skills,
        required_skills=None,
        final_score=None):

    strengths = identify_strengths(
        matched_skills
    )

    weaknesses = identify_weaknesses(
        missing_skills
    )

    recommended_role = recommend_role(
        strengths
    )

    summary = generate_summary(
        strengths,
        recommended_role
    )

    strength_summary = generate_strength_summary(
        strengths
    )

    weakness_summary = generate_weakness_summary(
        weaknesses
    )

    if required_skills is None:

        required_count = len(
            strengths
        ) + len(
            weaknesses
        )

    else:

        required_count = len(
            required_skills
        )

    gap_percentage = skill_gap_percentage(
        len(
            strengths
        ),
        required_count
    )

    insights = {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "strength_summary": strength_summary,
        "weakness_summary": weakness_summary,
        "skill_gap_percentage": gap_percentage,
        "recommended_role": recommended_role
    }

    if final_score is not None:

        insights[
            "final_score"
        ] = final_score

    return insights


def generate_copilot_insight(
        matched_skills,
        missing_skills,
        required_skills=None,
        final_score=None):

    return generate_insights(
        matched_skills,
        missing_skills,
        required_skills,
        final_score
    )