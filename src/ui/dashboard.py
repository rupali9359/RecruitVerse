import sys
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.api.database import (
    get_connection
)

from src.ui.analytics import (
    show_analytics_page
)


def show_dashboard():

    if not st.session_state.get(
            "logged_in"
    ):

        st.error(
            "Please Login First"
        )

        st.stop()

    st.sidebar.title(
        "RecruitVerse"
    )

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Dashboard",
            "Matching",
            "Rankings",
            "Analytics",
            "Recruiter Notes",
            "Interviews"
        ]
    )

    if st.sidebar.button(
            "Logout"
    ):

        st.session_state[
            "logged_in"
        ] = False

        st.session_state[
            "username"
        ] = None

        st.rerun()

    if menu == "Dashboard":

        st.title(
            "RecruitVerse Dashboard"
        )

        st.success(
            "Welcome to RecruitVerse"
        )

        st.write(
            "Use the sidebar to access matching, rankings, analytics, recruiter notes, and interviews."
        )

    elif menu == "Analytics":

        show_analytics_page()

    elif menu == "Recruiter Notes":

        st.title(
            "Recruiter Notes"
        )

        resume_name = st.text_input(
            "Resume Name"
        )

        note = st.text_area(
            "Note"
        )

        if st.button(
                "Save Note"
        ):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO recruiter_notes (
                    resume_name,
                    note
                )
                VALUES (%s, %s);
                """,
                (
                    resume_name,
                    note
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success(
                "Note saved successfully"
            )

    elif menu == "Interviews":

        st.title(
            "Interview Scheduler"
        )

        candidate_name = st.text_input(
            "Candidate Name"
        )

        interview_date = st.date_input(
            "Interview Date"
        )

        status = st.selectbox(
            "Status",
            [
                "Scheduled",
                "Completed",
                "Cancelled"
            ]
        )

        if st.button(
                "Schedule Interview"
        ):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO interviews (
                    candidate_name,
                    interview_date,
                    status
                )
                VALUES (%s, %s, %s);
                """,
                (
                    candidate_name,
                    interview_date,
                    status
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            st.success(
                "Interview scheduled successfully"
            )

    elif menu == "Rankings":

        st.title(
            "Candidate Rankings"
        )

        st.info(
            "Ranking module is available from the ranking engine."
        )

    elif menu == "Matching":

        st.title(
            "Candidate Matching"
        )

        st.info(
            "Matching module processes resumes against job descriptions."
        )


if __name__ == "__main__":

    show_dashboard()