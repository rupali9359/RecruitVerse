import psycopg2

from src.config.settings import (
    get_database_config
)


def get_connection():

    config = get_database_config()

    return psycopg2.connect(
        database=config[
            "database"
        ],
        user=config[
            "user"
        ],
        password=config[
            "password"
        ],
        host=config[
            "host"
        ],
        port=config[
            "port"
        ]
    )