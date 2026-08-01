# Customer Review Analysis

Customer Review Analysis is an end-to-end NLP project for sentiment classification of customer reviews from California gyms. The project combines web scraping, data cleaning, classical machine learning, transformer fine-tuning, and an interactive Streamlit app.

## Why this project is valuable
- Demonstrates a complete AI workflow from raw data to deployment-ready inference
- Combines traditional ML and modern transformer-based approaches
- Uses a realistic business problem: understanding customer sentiment at scale
- Provides a strong portfolio project for AI, NLP, and data science internships

## Project structure
```text
customer-review-analysis/
├── app.py
├── config.yaml
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   └── cleaned/
├── scripts/
│   ├── prepare_data.py
│   ├── augment_data.py
│   ├── train_classical_models.py
│   ├── train_finetuned_model.py
│   ├── evaluate_models.py
│   └── run_app.py
├── src/
│   └── customer_review_analysis/
│       ├── app.py
│       └── config.py
└── scraper/
```

## Workflow
1. Scraping: collect review data from Google Maps and other sources
2. Preparation: clean text, derive sentiment labels, and create train/test splits
3. Classical ML: train and evaluate Naive Bayes, Logistic Regression, and Random Forest baselines
4. Transformer fine-tuning: fine-tune an XLM-RoBERTa model for multilingual sentiment analysis
5. Evaluation: compare model performance with metrics such as accuracy and F1-score
6. Inference app: run a Streamlit interface for real-time predictions

## Setup
```bash
python -m pip install -r requirements.txt
python scripts/prepare_data.py
python scripts/train_classical_models.py
python scripts/train_finetuned_model.py
python scripts/evaluate_models.py
python scripts/run_app.py
```

## Configuration
The project uses [config.yaml](config.yaml) for all portable paths and defaults. You can override paths through environment variables such as:
- CUSTOMER_REVIEW_MODEL_PATH
- CUSTOMER_REVIEW_RAW_DATA
- CUSTOMER_REVIEW_CLEANED_DATA

## Notes
- The notebooks in the repository are kept for reference and experimentation.
- The scripts in [scripts/](scripts/) are the recommended entry points for reproducible runs.
- The Streamlit app loads the fine-tuned model from the configured path and will show a friendly message if the model is missing.

## Recommended next steps
- Add automated tests
- Add experiment tracking with MLflow or Weights & Biases
- Containerize the app with Docker
- Deploy the inference app to a cloud platform

