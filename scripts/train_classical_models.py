from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_path


def train_classical_models() -> None:
    train_path = get_path("ml_train_data", "data/cleaned/ml-methods-splits/train_set.csv")
    test_path = get_path("ml_test_data", "data/cleaned/ml-methods-splits/test_set.csv")
    model_dir = get_path("models_dir", "models")
    model_dir.mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(train_path, encoding="utf-8-sig")
    test_df = pd.read_csv(test_path, encoding="utf-8-sig")

    X_train, y_train = train_df["text"], train_df["label"]
    X_test, y_test = test_df["text"], test_df["label"]

    models = {
        "naive_bayes": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", ComplementNB()),
        ]),
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=2000, random_state=42)),
        ]),
        "random_forest": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", RandomForestClassifier(n_estimators=300, random_state=42)),
        ]),
    }

    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average="weighted")
        joblib.dump(pipeline, model_dir / f"{name}.joblib")
        print(f"{name}: accuracy={accuracy:.4f}, f1={f1:.4f}")


if __name__ == "__main__":
    train_classical_models()
