import streamlit as st
import pandas as pd

from src.services.analytics_service import (
    get_recruiter_analytics,
    get_search_history,
    get_top_skills
)


def show_analytics_page():

    st.title(
        "Recruiter Analytics Dashboard"
    )

    analytics = get_recruiter_analytics()

    col1, col2, col3 = st.columns(
        3
    )

    col1.metric(
        "Total Candidates",
        analytics[
            "total_candidates"
        ]
    )

    col2.metric(
        "Average Score",
        analytics[
            "average_score"
        ]
    )

    col3.metric(
        "Shortlisted %",
        analytics[
            "shortlisted_percent"
        ]
    )

    st.subheader(
        "Candidate Status Distribution"
    )

    status_counts = analytics[
        "status_counts"
    ]

    if status_counts:

        st.bar_chart(
            status_counts
        )

    else:

        st.info(
            "No candidate status data available yet."
        )

    st.subheader(
        "Top Skills"
    )

    top_skills = get_top_skills()

    if top_skills:

        df = pd.DataFrame(
            top_skills
        )

        st.dataframe(
            df
        )

        st.bar_chart(
            df.set_index(
                "skill"
            )
        )

    else:

        st.info(
            "No skill data available yet."
        )

    st.subheader(
        "Recruiter Search History"
    )

    history = get_search_history()

    if history:

        st.dataframe(
            pd.DataFrame(
                history
            )
        )

    else:

        st.info(
            "No search history available yet."
        )


if __name__ == "__main__":

    show_analytics_page()