import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def create_semantic_searches_table():

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_searches (
                id SERIAL PRIMARY KEY,
                query TEXT,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def save_semantic_search(
        query):

    if not query or not query.strip():
        return

    create_semantic_searches_table()

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO semantic_searches (
                query
            )
            VALUES (
                %s
            );
            """,
            (
                query.strip(),
            )
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_top_searches(
        limit=10):

    create_semantic_searches_table()

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                query,
                COUNT(*) AS search_count
            FROM semantic_searches
            GROUP BY query
            ORDER BY search_count DESC
            LIMIT %s;
            """,
            (
                limit,
            )
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()