import json
from functools import lru_cache
from pathlib import Path

import joblib


ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT_DIR
    / "models"
    / "candidate_scoring.pkl"
)

METRICS_PATH = (
    ROOT_DIR
    / "models"
    / "candidate_scoring_metrics.json"
)


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


def save_model_metrics(
        metrics):

    metrics[
        "model_name"
    ] = metrics.get(
        "model_name",
        "RandomForestRegressor"
    )

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
            METRICS_PATH,
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


def load_model_metrics():

    if METRICS_PATH.exists():

        with open(
                METRICS_PATH,
                "r",
                encoding="utf-8"
        ) as file:

            metrics = json.load(
                file
            )

        if "model_name" not in metrics:

            metrics[
                "model_name"
            ] = "RandomForestRegressor"

            save_model_metrics(
                metrics
            )

        return metrics

    return {
        "model_name": "RandomForestRegressor",
        "r2_score": None,
        "model_path": str(
            MODEL_PATH
        ),
        "status": "metrics_unavailable"
    }