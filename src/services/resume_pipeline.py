from src.ml_model.predict_score import (
    predict_candidate_score
)


def calculate_resume_score(
        keyword_score,
        semantic_score,
        matched,
        jd_skills):

    final_score = predict_candidate_score(
        keyword_score,
        semantic_score,
        len(matched),
        len(jd_skills)
    )

    return final_score