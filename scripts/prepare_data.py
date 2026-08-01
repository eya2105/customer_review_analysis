from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_path


def rating_to_sentiment(rating: float) -> str:
    if rating >= 4:
        return "positif"
    if rating == 3:
        return "neutre"
    return "negatif"


def clean_text_light(text: str) -> str:
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def prepare_data() -> None:
    raw_path = get_path("raw_data", "data/raw/all_california_gym_reviews.csv")
    cleaned_path = get_path("cleaned_data", "data/cleaned/cleaned_reviews_general.csv")
    finetuning_dir = get_path("finetuning_splits_dir", "data/cleaned/finetuning-splits")
    ml_dir = get_path("ml_splits_dir", "data/cleaned/ml-methods-splits")

    if not raw_path.exists():
        raise FileNotFoundError(f"Expected raw dataset at {raw_path}")

    df = pd.read_csv(raw_path, encoding="utf-8-sig")
    df = df.dropna(subset=["comment"])
    df = df[df["comment"].astype(str).str.strip() != ""]
    df = df.copy()
    df["sentiment"] = df["rating"].apply(rating_to_sentiment)
    df["comment_clean"] = df["comment"].apply(clean_text_light)
    df = df.drop(columns=["id", "name", "source", "location", "date", "comment"], errors="ignore")
    sentiment_map = {"negatif": 0, "neutre": 1, "positif": 2}
    df["sentiment_encoded"] = df["sentiment"].map(sentiment_map)

    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cleaned_path, index=False, encoding="utf-8-sig")

    finetuning_dir.mkdir(parents=True, exist_ok=True)
    finetuning_df = df[["comment_clean", "sentiment_encoded"]].rename(columns={"comment_clean": "text", "sentiment_encoded": "label"})
    finetuning_df = finetuning_df.dropna(subset=["text"])
    train_df, test_df = train_test_split(finetuning_df, test_size=0.2, random_state=42, stratify=finetuning_df["label"])
    train_df.to_csv(finetuning_dir / "train_set.csv", index=False, encoding="utf-8-sig")
    test_df.to_csv(finetuning_dir / "test_set.csv", index=False, encoding="utf-8-sig")

    ml_dir.mkdir(parents=True, exist_ok=True)
    ml_df = df[["comment_clean", "sentiment_encoded"]].rename(columns={"comment_clean": "text", "sentiment_encoded": "label"})
    ml_train_df, ml_test_df = train_test_split(ml_df, test_size=0.2, random_state=42, stratify=ml_df["label"])
    ml_train_df.to_csv(ml_dir / "train_set.csv", index=False, encoding="utf-8-sig")
    ml_test_df.to_csv(ml_dir / "test_set.csv", index=False, encoding="utf-8-sig")

    print(f"Prepared dataset saved to {cleaned_path}")
    print(f"Fine-tuning splits saved to {finetuning_dir}")
    print(f"ML splits saved to {ml_dir}")


if __name__ == "__main__":
    prepare_data()
