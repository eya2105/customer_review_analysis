import streamlit as st
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(page_title="Comparaison de Modèles NLP", layout="wide")

st.title("📊 Comparaison de modèles d'analyse de sentiments")

# ==============================
# CHARGEMENT DES DONNÉES TEST
# ==============================
@st.cache_data
def load_test_data():
    df = pd.read_csv("C:\\Users\\MSI\\Desktop\\customer_review_analysis\\data\\cleaned\\finetuning-splits\\test_set.csv")   # <-- adapte le chemin
    return df

test_df = load_test_data()
test_texts = test_df["text"].tolist()
true_labels = test_df["label"].tolist()

# ==============================
# CHARGEMENT DES MODÈLES
# ==============================
@st.cache_resource
def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return tokenizer, model

model_path_1 = "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\finetuning_models\\my_sentiment_model"
model_path_2 = "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\finetuning_models\\my_sentiment_model_without_augmentation"
model_path_3= "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\finetuning_models\\my_sentiment_model_data_augmentation"
model_path_4= "C:\\Users\\MSI\\Desktop\\customer_review_analysis\\finetuning_models\\my_sentiment_model_data_augmentation_not_cleaned"

tokenizer1, model1 = load_model(model_path_1)
tokenizer2, model2 = load_model(model_path_2)
tokenizer3, model3 = load_model(model_path_3)
tokenizer4, model4 = load_model(model_path_4)

# ==============================
# FONCTION D'ÉVALUATION
# ==============================
def evaluate_model(model, tokenizer, texts, true_labels):
    predictions = []

    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            predictions.append(pred)

    accuracy = accuracy_score(true_labels, predictions)
    report = classification_report(true_labels, predictions, output_dict=True)
    cm = confusion_matrix(true_labels, predictions, labels=np.unique(true_labels))

    return accuracy, report, cm, predictions

# ==============================
# ÉVALUATION DES DEUX MODÈLES
# ==============================
acc1, report1, cm1, preds1 = evaluate_model(model1, tokenizer1, test_texts, true_labels)
acc2, report2, cm2, preds2 = evaluate_model(model2, tokenizer2, test_texts, true_labels)
acc3, report3, cm3, preds3 = evaluate_model(model3, tokenizer3, test_texts, true_labels)
acc4, report4, cm4, preds4 = evaluate_model(model4, tokenizer4, test_texts, true_labels)

# ==============================
# COMPARAISON GLOBALE
# ==============================
st.subheader("📈 Comparaison Globale")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy - Modèle 1", round(acc1, 4)) 
    st.metric("F1-weighted - Modèle 1", round(report1["macro avg"]["f1-score"], 4))

with col2:
    st.metric("Accuracy - Modèle 2", round(acc2, 4))
    st.metric("F1-weighted - Modèle 2", round(report2["macro avg"]["f1-score"], 4))
with col3:
    st.metric("Accuracy - Modèle 3", round(acc3, 4))
    st.metric("F1-weighted - Modèle 3", round(report3["macro avg"]["f1-score"], 4))
with col4:
    st.metric("Accuracy - Modèle 4", round(acc4, 4))
    st.metric("F1-weighted - Modèle 4", round(report4["macro avg"]["f1-score"], 4))

# ==============================
# GRAPHIQUES ACCURACY & F1
# ==============================
st.subheader("📊 Graphiques de comparaison")

df_scores = pd.DataFrame({
    "Modèle": ["Modèle 1", "Modèle 2", "Modèle 3", "Modèle 4"],
    "Accuracy": [acc1, acc2, acc3, acc4],
    "F1-score": [
        report1["weighted avg"]["f1-score"],
        report2["weighted avg"]["f1-score"],
        report3["weighted avg"]["f1-score"],
        report4["weighted avg"]["f1-score"]
    ]
})

col5, col6 = st.columns(2)

with col5:
    st.bar_chart(df_scores.set_index("Modèle")["Accuracy"])

with col6:
    st.bar_chart(df_scores.set_index("Modèle")["F1-score"])


# ==============================
# MATRICES DE CONFUSION
# ==============================
st.subheader("🧮 Matrices de confusion")

col7, col8, col9, col10 = st.columns(4)

with col7:
    st.markdown("### Modèle 1")
    fig1, ax1 = plt.subplots()
    disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1)
    disp1.plot(ax=ax1)
    st.pyplot(fig1)

with col8:
    st.markdown("### Modèle 2")
    fig2, ax2 = plt.subplots()
    disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2)
    disp2.plot(ax=ax2)
    st.pyplot(fig2)
with col9:
    st.markdown("### Modèle 3")
    fig3, ax3 = plt.subplots()
    disp3 = ConfusionMatrixDisplay(confusion_matrix=cm3)
    disp3.plot(ax=ax3)
    st.pyplot(fig3)
with col10:
    st.markdown("### Modèle 4")
    fig4, ax4 = plt.subplots()
    disp4 = ConfusionMatrixDisplay(confusion_matrix=cm4)
    disp4.plot(ax=ax4)
    st.pyplot(fig4)

# ==============================
# TEST EN TEMPS RÉEL
# ==============================
st.subheader("🧠 Test en temps réel")

user_text = st.text_area("Entrez un commentaire client :")

if st.button("Analyser"):
    if user_text.strip() != "":
        inputs1 = tokenizer1(user_text, return_tensors="pt", truncation=True, padding=True)
        outputs1 = model1(**inputs1)
        probs1 = torch.softmax(outputs1.logits, dim=1)[0]
        pred1 = torch.argmax(probs1).item()

        inputs2 = tokenizer2(user_text, return_tensors="pt", truncation=True, padding=True)
        outputs2 = model2(**inputs2)
        probs2 = torch.softmax(outputs2.logits, dim=1)[0]
        pred2 = torch.argmax(probs2).item()

        inputs3 = tokenizer3(user_text, return_tensors="pt", truncation=True, padding=True)
        outputs3 = model3(**inputs3)
        probs3 = torch.softmax(outputs3.logits, dim=1)[0]
        pred3 = torch.argmax(probs3).item()

        inputs4 = tokenizer4(user_text, return_tensors="pt", truncation=True, padding=True)
        outputs4 = model4(**inputs4)
        probs4 = torch.softmax(outputs4.logits, dim=1)[0]
        pred4 = torch.argmax(probs4).item()

        col10, col11, col12, col13 = st.columns(4)

        with col10:
            st.markdown("### 🔵 Modèle 1")
            st.write("Classe prédite :", pred1)
            st.write("Probabilités :", probs1.tolist())

        with col11:
            st.markdown("### 🟢 Modèle 2")
            st.write("Classe prédite :", pred2)
            st.write("Probabilités :", probs2.tolist())
        with col12:
            st.markdown("### 🟠 Modèle 3")
            st.write("Classe prédite :", pred3)
            st.write("Probabilités :", probs3.tolist())
        with col13:
            st.markdown("### 🔴 Modèle 4")
            st.write("Classe prédite :", pred4)
            st.write("Probabilités :", probs4.tolist())
    else:
        st.warning("Veuillez entrer un texte.")
