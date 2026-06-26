from src.semantic_search.index_builder import (
    INDEX_PATH,
    build_index
)

from src.semantic_search.search_engine import (
    search_resumes
)


def semantic_resume_search(
        query,
        resume_folder="data/parsed_resumes/raw_text",
        top_k=10,
        rebuild=False):

    if rebuild or not INDEX_PATH.exists():
        build_index(
            resume_folder
        )

    results = search_resumes(
        query,
        top_k=top_k
    )

    return results


if __name__ == "__main__":

    query = (
        "Looking for a Data Scientist with Python, SQL, "
        "machine learning, NLP and analytics experience"
    )

    results = semantic_resume_search(
        query,
        top_k=3,
        rebuild=True
    )

    for resume_name, score in results:
        print(
            resume_name,
            score
        )