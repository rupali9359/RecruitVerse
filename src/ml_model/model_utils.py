from functools import lru_cache
from pathlib import Path

import joblib


ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT_DIR / "models" / "candidate_scoring.pkl"


@lru_cache(
    maxsize=1
)
def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model file not found. Run: python -m src.ml_model.train_model"
        )

    return joblib.load(
        MODEL_PATH
    )