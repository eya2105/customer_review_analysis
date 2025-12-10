import streamlit as st
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# ==============================
# CONFIGURATION DE LA PAGE
# ==============================
st.set_page_config(
    page_title="Analyse de Sentiment - XML-RoBERTa",
    layout="wide"
)

st.title("Analyse des commentaires clients – California Gym")
st.caption("Classification automatique des sentiments par intelligence artificielle")



st.divider()

# ==============================
# MAPPING DES CLASSES
# ==============================
label_map = {
    0: "Négatif",
    1: "Neutre",
    2: "Positif"
}

# ==============================
# CHARGEMENT DES DONNÉES TEST
# ==============================
@st.cache_data
def load_test_data():
    df = pd.read_csv(
        "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\data\\cleaned\\finetuning-splits\\test_set.csv"
    )
    return df

test_df = load_test_data()
test_texts = test_df["text"].tolist()
true_labels = test_df["label"].tolist()

# ==============================
# CHARGEMENT DU MODÈLE
# ==============================
@st.cache_resource
def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return tokenizer, model

model_path_3 = "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\finetuning_models\\my_sentiment_model_data_augmentation"
tokenizer3, model3 = load_model(model_path_3)

# ==============================
# SECTION TEST EN TEMPS RÉEL
# ==============================
st.subheader(" Test en temps réel")

st.markdown("Saisissez un commentaire client ci-dessous pour analyser automatiquement son sentiment.")

user_text = st.text_area(
    "Commentaire client :",
    placeholder="Exemple : Le service était rapide et le personnel très aimable."
)

if st.button(" Analyser le sentiment"):
    if user_text.strip() != "":

        inputs3 = tokenizer3(
            user_text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        outputs3 = model3(**inputs3)
        probs3 = torch.softmax(outputs3.logits, dim=1)[0].detach().numpy()
        pred3 = int(np.argmax(probs3))

        sentiment_pred = label_map[pred3]

        st.success(" Analyse terminée avec succès !")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Sentiment prédit")
            if sentiment_pred == "Positif":
                bg = "#d4edda"
                color = "#155724"
            elif sentiment_pred == "Négatif":
                  bg = "#f8d7da"
                  color = "#721c24"
            else:
                bg = "#fff3cd"
                color = "#856404"
            st.markdown(
                f"""
                <div style="
                    background-color: {bg};
                    color: {color};
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    font-size: 32px;
                    font-weight: bold;
                ">
                {sentiment_pred}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown("### Probabilités par classe")
            prob_df = pd.DataFrame({
                "Classe": ["Négatif", "Neutre", "Positif"],
                "Probabilité": probs3
            })
            st.dataframe(prob_df, use_container_width=True)

    else:
        st.warning("⚠️ Veuillez entrer un commentaire avant de lancer l’analyse.")

st.divider()


