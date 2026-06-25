import pandas as pd

from src.ml_model.model_utils import (
    load_model
)

from src.ml_model.prepare_data import (
    FEATURE_COLUMNS
)


def predict_candidate_score(
        keyword_score,
        semantic_score,
        matched_skills,
        total_skills):

    if total_skills <= 0:
        total_skills = 1

    matched_skills = min(
        matched_skills,
        total_skills
    )

    input_data = pd.DataFrame(
        [
            {
                "keyword_score": float(
                    keyword_score
                ),
                "semantic_score": float(
                    semantic_score
                ),
                "matched_skills": int(
                    matched_skills
                ),
                "total_skills": int(
                    total_skills
                )
            }
        ],
        columns=FEATURE_COLUMNS
    )

    model = load_model()

    prediction = model.predict(
        input_data
    )

    final_score = float(
        prediction[0]
    )

    final_score = max(
        0,
        min(
            100,
            final_score
        )
    )

    return round(
        final_score,
        2
    )