from src.api.database import (
    get_connection
)


def test_connection():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1;"
    )

    result = cursor.fetchone()

    cursor.close()

    conn.close()

    assert result[0] == 1