from pathlib import Path

import joblib
import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from src.semantic_search.embedding_store import (
    generate_embedding
)


ROOT_DIR = Path(__file__).resolve().parents[2]

INDEX_PATH = (
    ROOT_DIR
    / "vector_db"
    / "resume_embeddings.pkl"
)


def load_index():

    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            "Vector index not found. Run: python -m src.semantic_search.index_builder"
        )

    embeddings = joblib.load(
        INDEX_PATH
    )

    return embeddings


def search_resumes(
        query,
        top_k=10):

    embeddings = load_index()

    if not embeddings:
        return []

    query_vector = generate_embedding(
        query
    )

    query_vector = np.asarray(
        query_vector
    ).reshape(
        1,
        -1
    )

    resume_names = list(
        embeddings.keys()
    )

    resume_vectors = np.vstack(
        [
            np.asarray(
                embeddings[
                    resume_name
                ]
            )
            for resume_name in resume_names
        ]
    )

    scores = cosine_similarity(
        query_vector,
        resume_vectors
    )[0]

    results = []

    for resume_name, score in zip(
            resume_names,
            scores):

        results.append(
            (
                resume_name,
                round(
                    float(score),
                    4
                )
            )
        )

    results.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return results[
        :top_k
    ]


if __name__ == "__main__":

    query = (
        "Data scientist with Python, SQL, machine learning, NLP, "
        "statistics and data visualization"
    )

    matches = search_resumes(
        query,
        top_k=5
    )

    for resume_name, score in matches:
        print(
            resume_name,
            score
        )