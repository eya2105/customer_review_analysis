# Customer Review Analysis — NLP Sentiment Classification

A full pipeline for scraping, preprocessing, and classifying gym reviews using both classical ML and transformer fine-tuning.

## Pipeline
1. **Scraping** — Selenium-based scraper collecting Google Maps reviews across California gyms
2. **Preprocessing** — Cleaning, language detection, data augmentation, train/test splitting
3. **ML Models** — Naïve Bayes, Logistic Regression, Random Forest benchmarked on original and augmented data
4. **Fine-tuning** — Transformer model fine-tuned on the cleaned dataset (team contribution)
5. **Evaluation** — F1-score comparison across all models

## Tech Stack
Python · scikit-learn · HuggingFace Transformers · Selenium · pandas · nltk

## Setup
```bash
pip install -r requirements.txt
```
