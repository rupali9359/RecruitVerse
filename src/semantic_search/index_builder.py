from pathlib import Path

import joblib

from src.semantic_search.embedding_store import (
    generate_embedding
)


ROOT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_RESUME_FOLDER = (
    ROOT_DIR
    / "data"
    / "parsed_resumes"
    / "raw_text"
)

VECTOR_DB_DIR = (
    ROOT_DIR
    / "vector_db"
)

INDEX_PATH = (
    VECTOR_DB_DIR
    / "resume_embeddings.pkl"
)


def build_index(
        resume_folder=DEFAULT_RESUME_FOLDER):

    resume_folder = Path(
        resume_folder
    )

    if not resume_folder.is_absolute():
        resume_folder = (
            ROOT_DIR
            / resume_folder
        )

    if not resume_folder.exists():
        raise FileNotFoundError(
            f"Resume folder not found: {resume_folder}"
        )

    embeddings = {}

    for file_path in sorted(
        resume_folder.iterdir()
    ):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() != ".txt":
            continue

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        if not text.strip():
            continue

        vector = generate_embedding(
            text
        )

        embeddings[
            file_path.name
        ] = vector

        print(
            "Indexed:",
            file_path.name
        )

    VECTOR_DB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        embeddings,
        INDEX_PATH
    )

    print(
        "Total resumes indexed:",
        len(embeddings)
    )

    print(
        "Index saved at:",
        INDEX_PATH
    )

    return embeddings


if __name__ == "__main__":
    build_index(
        "data/parsed_resumes/raw_text"
    )