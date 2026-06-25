from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = ROOT_DIR / "data" / "training" / "candidate_scores.csv"

FEATURE_COLUMNS = [
    "keyword_score",
    "semantic_score",
    "matched_skills",
    "total_skills"
]

TARGET_COLUMN = "final_score"


def create_sample_dataset_if_missing():
    if DATASET_PATH.exists():
        return

    DATASET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []

    for keyword_score in range(45, 101, 5):
        for semantic_score in range(45, 101, 5):
            for total_skills in [
                5,
                8,
                10,
                12,
                15
            ]:
                for skill_ratio in [
                    0.2,
                    0.4,
                    0.6,
                    0.8,
                    1.0
                ]:
                    matched_skills = max(
                        1,
                        round(total_skills * skill_ratio)
                    )

                    final_score = (
                        keyword_score * 0.35
                    ) + (
                        semantic_score * 0.45
                    ) + (
                        (matched_skills / total_skills) * 20
                    )

                    final_score = round(
                        min(
                            100,
                            final_score
                        ),
                        2
                    )

                    rows.append(
                        {
                            "keyword_score": keyword_score,
                            "semantic_score": semantic_score,
                            "matched_skills": matched_skills,
                            "total_skills": total_skills,
                            "final_score": final_score
                        }
                    )

    df = pd.DataFrame(
        rows
    )

    df.to_csv(
        DATASET_PATH,
        index=False
    )


def load_dataset():
    create_sample_dataset_if_missing()

    df = pd.read_csv(
        DATASET_PATH
    )

    required_columns = FEATURE_COLUMNS + [
        TARGET_COLUMN
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in dataset: {missing_columns}"
        )

    return df


def split_features_and_target(
        df):

    x = df[
        FEATURE_COLUMNS
    ]

    y = df[
        TARGET_COLUMN
    ]

    return x, y


if __name__ == "__main__":
    dataset = load_dataset()

    print(
        "Dataset loaded from:",
        DATASET_PATH
    )

    print(
        dataset.head()
    )

    x, y = split_features_and_target(
        dataset
    )

    print(
        "Features shape:",
        x.shape
    )

    print(
        "Target shape:",
        y.shape
    )