from src.services.shortlisting import (
    shortlist_candidate
)

from src.services.recommendation_engine import (
    generate_recommendation
)


def test_shortlist_candidate():

    assert shortlist_candidate(
        90
    ) == "Shortlisted"

    assert shortlist_candidate(
        70
    ) == "Rejected"


def test_generate_recommendation():

    assert "Strong Candidate" in generate_recommendation(
        90,
        []
    )

    assert "Good Candidate" in generate_recommendation(
        82,
        [
            "AWS"
        ]
    )

    assert "Weak Match" in generate_recommendation(
        50,
        [
            "AWS",
            "Docker",
            "SQL"
        ]
    )

from pathlib import Path

from src.services.archive_service import (
    archive_resume
)

from src.utils.email_service import (
    send_email
)

from src.utils.performance import (
    get_execution_time
)


def test_email_dry_run():

    result = send_email(
        "hr@example.com",
        "Top Candidate",
        "Candidate scored 92"
    )

    assert result[
        "success"
    ]


def test_archive_resume():

    test_file = Path(
        "tests/archive_test_resume.pdf"
    )

    test_file.write_text(
        "dummy resume",
        encoding="utf-8"
    )

    archived_path = archive_resume(
        test_file
    )

    assert archived_path.exists()


def test_performance_time():

    import time

    start = time.time()

    time.sleep(
        0.1
    )

    execution_time = get_execution_time(
        start
    )

    assert execution_time >= 0