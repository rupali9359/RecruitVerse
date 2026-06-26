import os
import sys
from pathlib import Path

import psycopg2
import streamlit as st
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


load_dotenv()


from src.semantic_search.vector_search import (
    semantic_resume_search
)

from src.semantic_search.search_history import (
    save_semantic_search,
    get_top_searches
)


try:
    from src.api.database import (
        get_connection
    )
except Exception:
    def get_connection():
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )


try:
    from src.ui.analytics import (
        show_analytics_page as existing_analytics_page
    )
except Exception:
    existing_analytics_page = None


try:
    from src.ui.ai_copilot import (
        show_ai_copilot_page
    )
except Exception:
    show_ai_copilot_page = None


def ensure_dashboard_tables():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recruiter_notes (
                id SERIAL PRIMARY KEY,
                resume_name TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interviews (
                id SERIAL PRIMARY KEY,
                candidate_name TEXT,
                interview_date DATE,
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def show_home_page():

    st.title(
        "RecruitVerse Dashboard"
    )

    username = st.session_state.get(
        "username",
        "Recruiter"
    )

    st.write(
        f"Welcome Recruiter, {username}"
    )

    st.success(
        "Welcome to RecruitVerse"
    )

    st.write(
        "Use the sidebar to access matching, rankings, analytics, semantic search, AI Copilot, recruiter notes, and interviews."
    )

    st.divider()

    st.subheader(
        "RecruitVerse Status"
    )

    st.write(
        "Recruiter Login"
    )

    st.write(
        "Resume Upload"
    )

    st.write(
        "Matching Engine"
    )

    st.write(
        "Semantic Search"
    )

    st.write(
        "ML Scoring"
    )

    st.write(
        "Ranking"
    )

    st.write(
        "Analytics"
    )


def show_semantic_search_page():

    st.title(
        "Semantic Resume Search"
    )

    st.write(
        "Search candidates using meaning-based resume similarity."
    )

    query = st.text_input(
        "Search Candidates",
        placeholder="Example: Python SQL Machine Learning"
    )

    top_k = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button(
        "Search"
    ):

        if not query.strip():

            st.error(
                "Please enter a search query"
            )

        else:

            try:

                with st.spinner(
                    "Searching resumes..."
                ):

                    results = semantic_resume_search(
                        query,
                        top_k=top_k
                    )

                    save_semantic_search(
                        query
                    )

                st.session_state[
                    "last_search_results"
                ] = results

                if not results:

                    st.warning(
                        "No matching resumes found"
                    )

                else:

                    st.success(
                        "Top matching resumes"
                    )

            except FileNotFoundError:

                st.error(
                    "Vector index not found. Please build the resume index first."
                )

                st.code(
                    "python -m src.semantic_search.index_builder"
                )

            except Exception as error:

                st.error(
                    "Search failed"
                )

                st.write(
                    error
                )

    results = st.session_state.get(
        "last_search_results",
        []
    )

    if results:

        st.divider()

        st.subheader(
            "Results"
        )

        for resume, score in results:

            st.write(
                resume,
                round(
                    score,
                    2
                )
            )


def show_semantic_search_analytics():

    st.subheader(
        "Semantic Search Analytics"
    )

    try:

        top_searches = get_top_searches(
            limit=5
        )

        if top_searches:

            for search_query, count in top_searches:

                st.write(
                    search_query,
                    count
                )

        else:

            st.info(
                "No searches recorded yet"
            )

    except Exception as error:

        st.error(
            "Could not load search analytics"
        )

        st.write(
            error
        )


def show_analytics_menu_page():

    if existing_analytics_page:

        try:
            existing_analytics_page()

        except Exception as error:
            st.title(
                "Analytics"
            )

            st.warning(
                "Main analytics page could not load."
            )

            st.write(
                error
            )

    else:

        st.title(
            "Analytics"
        )

        st.info(
            "Analytics module is not available yet."
        )

    st.divider()

    show_semantic_search_analytics()


def show_recruiter_notes_page():

    ensure_dashboard_tables()

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

        if not resume_name.strip() or not note.strip():

            st.error(
                "Please enter resume name and note"
            )

        else:

            conn = None
            cursor = None

            try:
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

                st.success(
                    "Note saved successfully"
                )

            except Exception as error:

                st.error(
                    "Failed to save note"
                )

                st.write(
                    error
                )

            finally:

                if cursor:
                    cursor.close()

                if conn:
                    conn.close()

    st.divider()

    st.subheader(
        "Recent Notes"
    )

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                resume_name,
                note,
                created_at
            FROM recruiter_notes
            ORDER BY created_at DESC
            LIMIT 10;
            """
        )

        notes = cursor.fetchall()

        if notes:

            for item_resume_name, item_note, created_at in notes:

                st.write(
                    item_resume_name,
                    item_note,
                    created_at
                )

        else:

            st.info(
                "No notes saved yet"
            )

    except Exception as error:

        st.warning(
            "Could not load notes"
        )

        st.write(
            error
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def show_interviews_page():

    ensure_dashboard_tables()

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

        if not candidate_name.strip():

            st.error(
                "Please enter candidate name"
            )

        else:

            conn = None
            cursor = None

            try:
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

                st.success(
                    "Interview scheduled successfully"
                )

            except Exception as error:

                st.error(
                    "Failed to schedule interview"
                )

                st.write(
                    error
                )

            finally:

                if cursor:
                    cursor.close()

                if conn:
                    conn.close()

    st.divider()

    st.subheader(
        "Recent Interviews"
    )

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                candidate_name,
                interview_date,
                status,
                created_at
            FROM interviews
            ORDER BY created_at DESC
            LIMIT 10;
            """
        )

        interviews = cursor.fetchall()

        if interviews:

            for candidate, date, item_status, created_at in interviews:

                st.write(
                    candidate,
                    date,
                    item_status,
                    created_at
                )

        else:

            st.info(
                "No interviews scheduled yet"
            )

    except Exception as error:

        st.warning(
            "Could not load interviews"
        )

        st.write(
            error
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def show_matching_page():

    st.title(
        "Candidate Matching"
    )

    st.info(
        "Matching module processes resumes against job descriptions."
    )


def show_rankings_page():

    st.title(
        "Candidate Rankings"
    )

    st.info(
        "Ranking module is available from the ranking engine."
    )


def show_ai_copilot_menu_page():

    if show_ai_copilot_page:

        show_ai_copilot_page()

    else:

        st.title(
            "AI Copilot"
        )

        st.info(
            "AI Copilot module is not available yet."
        )


def show_dashboard():

    if not st.session_state.get(
        "logged_in"
    ):

        st.error(
            "Please Login First"
        )

        st.stop()

    if "last_search_results" not in st.session_state:

        st.session_state[
            "last_search_results"
        ] = []

    st.sidebar.title(
        "RecruitVerse"
    )

    username = st.session_state.get(
        "username",
        "Recruiter"
    )

    st.sidebar.write(
        f"Logged in as: {username}"
    )

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Dashboard",
            "Matching",
            "Semantic Search",
            "Rankings",
            "Analytics",
            "AI Copilot",
            "Recruiter Notes",
            "Interviews"
        ]
    )

    st.sidebar.markdown(
        "---"
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

        st.session_state[
            "last_search_results"
        ] = []

        st.rerun()

    if menu == "Dashboard":

        show_home_page()

    elif menu == "Matching":

        show_matching_page()

    elif menu == "Semantic Search":

        show_semantic_search_page()

    elif menu == "Rankings":

        show_rankings_page()

    elif menu == "Analytics":

        show_analytics_menu_page()

    elif menu == "AI Copilot":

        show_ai_copilot_menu_page()

    elif menu == "Recruiter Notes":

        show_recruiter_notes_page()

    elif menu == "Interviews":

        show_interviews_page()


if __name__ == "__main__":

    show_dashboard()