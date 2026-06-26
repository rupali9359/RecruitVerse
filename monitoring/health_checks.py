from src.api.database import (
    get_connection
)

from src.utils.logger import (
    get_logger
)


logger = get_logger(
    "recruitverse.health"
)


def check_database():

    conn = None
    cursor = None

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1;"
        )

        result = cursor.fetchone()

        return result[
            0
        ] == 1

    except Exception as error:

        logger.exception(
            "Database health check failed: %s",
            error
        )

        return False

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_health_status():

    database_status = check_database()

    return {
        "api": "UP",
        "database": database_status
    }


if __name__ == "__main__":

    print(
        get_health_status()
    )