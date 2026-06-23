import streamlit as st


def show_dashboard():

    if not st.session_state.get(
        "logged_in"
    ):

        st.error(
            "Please Login First"
        )

        st.stop()

    st.sidebar.title(
        "Sidebar"
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
        "RecruitVerse Dashboard Opens"
    )

    st.write(
        "You are successfully logged in."
    )


if __name__ == "__main__":
    show_dashboard()