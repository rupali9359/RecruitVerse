from pathlib import Path

import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from src.ml_model.prepare_data import (
    load_dataset,
    split_features_and_target
)


ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT_DIR / "models" / "candidate_scoring.pkl"


def train_candidate_scoring_model():
    df = load_dataset()

    x, y = split_features_and_target(
        df
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        x_train,
        y_train
    )

    predictions = model.predict(
        x_test
    )

    score = r2_score(
        y_test,
        predictions
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        "Model trained successfully"
    )

    print(
        "R2 Score:",
        round(
            score,
            4
        )
    )

    print(
        "Model saved at:",
        MODEL_PATH
    )

    return model


if __name__ == "__main__":
    train_candidate_scoring_model()