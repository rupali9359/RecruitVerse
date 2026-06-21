import os
import psycopg2
from dotenv import load_dotenv

from auth_service import (
    hash_password
)


load_dotenv()


def register_user(
        username,
        email,
        password):

    password_hash = hash_password(password)

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (
                %s,
                %s,
                %s
            )
            RETURNING id;
            """,
            (
                username,
                email,
                password_hash
            )
        )

        user_id = cursor.fetchone()[0]

        connection.commit()

        print("User registered successfully")
        print("User ID:", user_id)

        return user_id

    except psycopg2.errors.UniqueViolation:
        if connection:
            connection.rollback()

        print("Username or email already exists")
        return None

    except Exception as error:
        if connection:
            connection.rollback()

        print("Registration failed")
        print(error)
        return None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    register_user(
        "testuser",
        "testuser@example.com",
        "root123"
    )