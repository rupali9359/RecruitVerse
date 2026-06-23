import os
import psycopg2
from dotenv import load_dotenv

try:
    from src.auth.auth_service import (
        verify_password
    )
except ModuleNotFoundError:
    from auth_service import (
        verify_password
    )


load_dotenv()


def login_user(
        username,
        password):

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                password_hash
            FROM users
            WHERE username=%s
            """,
            (
                username,
            )
        )

        user = cursor.fetchone()

        if user:
            return verify_password(
                password,
                user[0]
            )

        return False

    except Exception as error:
        print("Login failed")
        print(error)
        return False

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    print(
        login_user(
            "testuser",
            "root123"
        )
    )