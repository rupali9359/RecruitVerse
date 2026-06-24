import sys
from pathlib import Path

import psycopg2


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
    hash_password
)


def register_user(
        username,
        email,
        password):

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(
                username,
                email,
                password_hash
            )
            VALUES
            (%s,%s,%s)
            RETURNING id;
            """,
            (
                username,
                email,
                hash_password(
                    password
                )
            )
        )

        user_id = cursor.fetchone()[0]

        conn.commit()

        print(
            "User registered successfully"
        )

        print(
            "User ID:",
            user_id
        )

        return user_id

    except psycopg2.errors.UniqueViolation:
        if conn:
            conn.rollback()

        print(
            "Username or email already exists"
        )

        return None

    except Exception as error:
        if conn:
            conn.rollback()

        print(
            "Registration failed"
        )

        print(
            error
        )

        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    register_user(
        "testuser_docker_check",
        "testuser_docker_check@example.com",
        "root123"
    )