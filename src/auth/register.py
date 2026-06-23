import os
import psycopg2
from dotenv import load_dotenv

try:
    from src.auth.auth_service import (
        hash_password
    )
except ModuleNotFoundError:
    from auth_service import (
        hash_password
    )

load_dotenv()


def register_user(
        username,
        email,
        password):

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
            hash_password(password)
        )
    )

    user_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()

    conn.close()

    print("User registered successfully")
    print("User ID:", user_id)

    return user_id


if __name__ == "__main__":
    register_user(
        "testuser4",
        "testuser4@example.com",
        "root123"
    )