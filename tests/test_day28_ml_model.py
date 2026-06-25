from pathlib import Path

from src.ml_model.model_utils import (
    MODEL_PATH,
    load_model,
    load_model_metrics
)

from src.ml_model.predict_score import (
    predict_candidate_score
)


def test_model_file_exists():

    assert Path(
        MODEL_PATH
    ).exists()


def test_model_loads():

    model = load_model()

    assert model is not None


def test_prediction_range():

    score = predict_candidate_score(
        75,
        82,
        6,
        8
    )

    assert score >= 0

    assert score <= 100


def test_prediction_reasonable():

    score = predict_candidate_score(
        75,
        82,
        6,
        8
    )

    assert score >= 70


def test_metrics_file_loads():

    metrics = load_model_metrics()

    assert "model_name" in metrics