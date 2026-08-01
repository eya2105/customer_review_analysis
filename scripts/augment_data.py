from __future__ import annotations

import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_path


try:
    from deep_translator import GoogleTranslator
    from sentence_transformers import SentenceTransformer, util
except ImportError:  # pragma: no cover - optional dependency path
    GoogleTranslator = None
    SentenceTransformer = None
    util = None


def back_translate_fr(text: str, pivot: str = "en") -> str | None:
    if GoogleTranslator is None:
        return None
    try:
        inter = GoogleTranslator(source="fr", target=pivot).translate(text)
        if not inter or len(inter.strip()) < 3:
            return None
        back = GoogleTranslator(source=pivot, target="fr").translate(inter)
        if not back or back.strip() == "" or back.strip() == text.strip():
            return None
        return back
    except Exception:
        return None


def is_semantic_sim(orig: str, aug: str, threshold: float = 0.80) -> bool:
    if SentenceTransformer is None or util is None:
        return True
    embed_model = SentenceTransformer("dangvantuan/sentence-camembert-base")
    emb_o = embed_model.encode(orig, convert_to_tensor=True)
    emb_a = embed_model.encode(aug, convert_to_tensor=True)
    return util.cos_sim(emb_o, emb_a).item() >= threshold


def augment_data() -> None:
    random.seed(42)
    np.random.seed(42)

    input_path = get_path("ml_splits_train", "data/cleaned/ml-methods-splits/train_set.csv")
    output_path = get_path("augmented_train_data", "data/cleaned/ml-methods-splits/augmented_train_set.csv")

    if not input_path.exists():
        raise FileNotFoundError(f"Expected training split at {input_path}")

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    augmented_rows = []
    for _, row in df.iterrows():
        text = str(row["text"])
        augmented = back_translate_fr(text)
        if augmented and is_semantic_sim(text, augmented):
            augmented_rows.append({"text": augmented, "label": row["label"]})
        else:
            augmented_rows.append({"text": text, "label": row["label"]})

    augmented_df = pd.DataFrame(augmented_rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    augmented_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Augmented data saved to {output_path}")


if __name__ == "__main__":
    augment_data()
