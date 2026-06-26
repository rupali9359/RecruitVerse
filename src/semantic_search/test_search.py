from src.semantic_search.vector_search import (
    semantic_resume_search
)


def test_semantic_search():

    query = (
        "Python SQL Machine Learning Data Science"
    )

    results = semantic_resume_search(
        query,
        top_k=5,
        rebuild=False
    )

    print(
        "Search Query:",
        query
    )

    print(
        "Results:"
    )

    for resume_name, score in results:

        print(
            resume_name,
            score
        )


if __name__ == "__main__":

    test_semantic_search()