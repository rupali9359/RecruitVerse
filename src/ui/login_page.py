import sys
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.auth.register import (
    register_user
)

from src.auth.login import (
    login_user
)

from src.ui.dashboard import (
    show_dashboard
)


st.set_page_config(
    page_title="RecruitVerse Auth",
    page_icon="🔐"
)


if "logged_in" not in st.session_state:
    st.session_state[
        "logged_in"
    ] = False


if "username" not in st.session_state:
    st.session_state[
        "username"
    ] = None


if st.session_state.get(
    "logged_in"
):

    show_dashboard()

    st.stop()


st.title(
    "RecruitVerse Authentication"
)


register_tab, login_tab = st.tabs(
    [
        "Register",
        "Login"
    ]
)


with register_tab:

    st.header(
        "RecruitVerse Registration"
    )

    register_username = st.text_input(
        "Username",
        key="register_username"
    )

    register_email = st.text_input(
        "Email",
        key="register_email"
    )

    register_password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button(
        "Register"
    ):

        if not register_username or not register_email or not register_password:

            st.error(
                "Please fill all fields"
            )

        else:

            user_id = register_user(
                register_username,
                register_email,
                register_password
            )

            if user_id:

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "Registration failed. Username or email may already exist."
                )


with login_tab:

    st.header(
        "RecruitVerse Login"
    )

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login"
    ):

        if not username or not password:

            st.error(
                "Please enter username and password"
            )

        else:

            success = login_user(
                username,
                password
            )

            if success:

                st.session_state[
                    "logged_in"
                ] = True

                st.session_state[
                    "username"
                ] = username

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )