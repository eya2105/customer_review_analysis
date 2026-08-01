from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_model_path, get_path


st.set_page_config(page_title="Customer Review Analysis", layout="wide")


LABEL_MAP = {0: "Negatif", 1: "Neutre", 2: "Positif"}


@st.cache_data
def load_test_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


@st.cache_resource
def load_model(model_path: Path):
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_path))
    model.eval()
    return tokenizer, model


def main() -> None:
    st.title("Customer Review Analysis")
    st.caption("Sentiment classification for gym reviews with transformers")

    test_data_path = get_path("finetuning_test_data", "data/cleaned/finetuning-splits/test_set.csv")
    if not test_data_path.exists():
        st.warning("Test data was not found. Run the preparation script first.")
        return

    model_path = get_model_path("finetuning_models/my_sentiment_model_data_augmentation")
    if not model_path.exists():
        st.warning("A fine-tuned model was not found. Train one with the training scripts first.")
        return

    test_df = load_test_data(test_data_path)
    test_texts = test_df["text"].tolist()
    true_labels = test_df["label"].tolist()

    tokenizer, model = load_model(model_path)

    st.subheader("Real-time prediction")
    user_text = st.text_area("Customer review", placeholder="Example: The staff was helpful and the gym was clean.")
    if st.button("Analyze sentiment"):
        if not user_text.strip():
            st.warning("Please enter a review before running the inference.")
            return

        inputs = tokenizer(user_text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)[0].detach().cpu().numpy()
        prediction = int(np.argmax(probabilities))
        sentiment = LABEL_MAP[prediction]

        st.success("Prediction completed")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Predicted sentiment")
            st.markdown(
                f"<div style='padding:24px;border-radius:12px;background:#f0f7ff;text-align:center;font-size:32px;font-weight:700'>{sentiment}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("### Probabilities")
            probability_df = pd.DataFrame({"Class": [LABEL_MAP[i] for i in range(3)], "Probability": probabilities})
            st.dataframe(probability_df, use_container_width=True)


if __name__ == "__main__":
    main()
