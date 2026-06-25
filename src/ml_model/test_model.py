from src.ml_model.predict_score import (
    predict_candidate_score
)


score = predict_candidate_score(
    75,
    82,
    6,
    8
)

print(
    score
)