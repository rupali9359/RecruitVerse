from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(
        MODEL_NAME
    )


def generate_embedding(text):
    text = (
        text or ""
    ).strip()

    if not text:
        text = " "

    model = get_embedding_model()

    vector = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return vector