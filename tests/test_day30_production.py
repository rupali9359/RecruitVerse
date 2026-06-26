def test_settings_load():

    from src.config.settings import (
        settings_summary
    )

    settings = settings_summary()

    assert settings[
        "app_name"
    ] == "RecruitVerse"

    assert settings[
        "db_name"
    ] == "recruiters"


def test_database_connection():

    from src.api.database import (
        get_connection
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1;"
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    assert result[
        0
    ] == 1


def test_health_check():

    from monitoring.health_checks import (
        get_health_status
    )

    health = get_health_status()

    assert health[
        "api"
    ] == "UP"

    assert health[
        "database"
    ] is True


def test_fastapi_app_imports():

    from src.api.main import (
        app
    )

    assert app.title