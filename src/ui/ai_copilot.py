import sys
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.ai_insights.recruiter_copilot import (
    generate_insights
)

from src.services.save_ai_insights import (
    get_saved_ai_insights,
    save_ai_insight
)


def parse_skills(
        text):

    if not text:

        return []

    text = text.replace(
        "\n",
        ","
    )

    return [
        skill.strip()
        for skill in text.split(
            ","
        )
        if skill.strip()
    ]


def show_ai_copilot_page():

    st.title(
        "AI Recruiter Copilot"
    )

    st.write(
        "Generate recruiter-friendly insights from candidate matching results."
    )

    resume_name = st.text_input(
        "Resume Name",
        value="john_resume.pdf"
    )

    matched_skills_text = st.text_area(
        "Matched Skills",
        value="Python, SQL, Machine Learning"
    )

    missing_skills_text = st.text_area(
        "Missing Skills",
        value="AWS, Tableau"
    )

    required_skills_text = st.text_area(
        "Required Skills",
        value="Python, SQL, Machine Learning, AWS, Tableau"
    )

    final_score = st.number_input(
        "Final Score",
        min_value=0.0,
        max_value=100.0,
        value=86.0
    )

    if st.button(
            "Generate AI Insights"
    ):

        matched_skills = parse_skills(
            matched_skills_text
        )

        missing_skills = parse_skills(
            missing_skills_text
        )

        required_skills = parse_skills(
            required_skills_text
        )

        insights = generate_insights(
            matched_skills,
            missing_skills,
            required_skills,
            final_score
        )

        st.session_state[
            "latest_ai_insights"
        ] = insights

        st.session_state[
            "latest_resume_name"
        ] = resume_name

    if st.session_state.get(
            "latest_ai_insights"
    ):

        insights = st.session_state[
            "latest_ai_insights"
        ]

        st.subheader(
            "AI Recruiter Insights"
        )

        st.info(
            insights[
                "summary"
            ]
        )

        st.metric(
            "Recommended Role",
            insights[
                "recommended_role"
            ]
        )

        st.metric(
            "Skill Gap %",
            insights[
                "skill_gap_percentage"
            ]
        )

        if "final_score" in insights:

            st.metric(
                "Final Score",
                insights[
                    "final_score"
                ]
            )

        st.subheader(
            "Strengths"
        )

        if insights[
                "strengths"
        ]:

            for skill in insights[
                    "strengths"
            ]:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.warning(
                "No strengths identified."
            )

        st.subheader(
            "Areas for Improvement"
        )

        if insights[
                "weaknesses"
        ]:

            for skill in insights[
                    "weaknesses"
            ]:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "No major weaknesses identified."
            )

        if st.button(
                "Save AI Insights"
        ):

            result = save_ai_insight(
                st.session_state.get(
                    "latest_resume_name",
                    "unknown_resume.pdf"
                ),
                insights
            )

            if result[
                    "success"
            ]:

                st.success(
                    result[
                        "message"
                    ]
                )

            else:

                st.error(
                    result[
                        "message"
                    ]
                )

    st.divider()

    st.subheader(
        "Saved AI Insights"
    )

    try:

        saved_insights = get_saved_ai_insights()

        if saved_insights:

            st.dataframe(
                saved_insights
            )

        else:

            st.info(
                "No saved AI insights yet."
            )

    except Exception as error:

        st.warning(
            f"Unable to load saved insights: {error}"
        )


if __name__ == "__main__":

    show_ai_copilot_page()