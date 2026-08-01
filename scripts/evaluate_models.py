from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_path


def evaluate_models() -> None:
    test_path = get_path("ml_test_data", "data/cleaned/ml-methods-splits/test_set.csv")
    test_df = pd.read_csv(test_path, encoding="utf-8-sig")
    X_test = test_df["text"]
    y_test = test_df["label"]

    model_dir = get_path("models_dir", "models")
    results = {}
    for model_path in sorted(model_dir.glob("*.joblib")):
        model = joblib.load(model_path)
        predictions = model.predict(X_test)
        results[model_path.stem] = {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "f1": round(float(f1_score(y_test, predictions, average="weighted")), 4),
            "precision": round(float(precision_score(y_test, predictions, average="weighted")), 4),
            "recall": round(float(recall_score(y_test, predictions, average="weighted")), 4),
        }

    output_path = get_path("evaluation_results", "evaluation/evaluation_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    evaluate_models()
