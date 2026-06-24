from src.ranking.ranking_engine import (
    rank_candidates
)


def test_ranking():

    candidates = [
        {
            "name": "A",
            "score": 80
        },
        {
            "name": "B",
            "score": 95
        }
    ]

    ranked = rank_candidates(
        candidates
    )

    assert ranked[0][
        "score"
    ] == 95

    assert ranked[0][
        "name"
    ] == "B"