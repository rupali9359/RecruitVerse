def rank_candidates(
        candidates):

    return sorted(
        candidates,
        key=lambda candidate: candidate.get(
            "score",
            0
        ),
        reverse=True
    )