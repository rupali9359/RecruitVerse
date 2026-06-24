import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.api.database import (
    get_connection
)

from src.auth.auth_service import (
    verify_password
)


def login_user(
        username,
        password):

    conn = None
    cursor = None

    try:
        conn = get_connection()

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
        print(
            "Login failed"
        )

        print(
            error
        )

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