from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import torch
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_path


def train_finetuned_model() -> None:
    train_path = get_path("finetuning_train_data", "data/cleaned/finetuning-splits/train_set.csv")
    model_output_dir = get_path("finetuning_models_dir", "finetuning_models/my_sentiment_model_data_augmentation")
    model_output_dir.mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(train_path, encoding="utf-8-sig")
    train_df = train_df.rename(columns={"text": "sentence", "label": "label"})
    dataset = Dataset.from_pandas(train_df[["sentence", "label"]])

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

    def tokenize(batch):
        return tokenizer(batch["sentence"], padding="max_length", truncation=True, max_length=128)

    tokenized_dataset = dataset.map(tokenize, batched=True)
    tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    model = AutoModelForSequenceClassification.from_pretrained("xlm-roberta-base", num_labels=3)
    training_args = TrainingArguments(
        output_dir=str(model_output_dir),
        per_device_train_batch_size=8,
        num_train_epochs=1,
        learning_rate=2e-5,
        save_strategy="epoch",
        logging_steps=10,
        report_to="none",
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_dataset)
    trainer.train()
    trainer.save_model(str(model_output_dir))
    tokenizer.save_pretrained(str(model_output_dir))
    print(f"Fine-tuned model saved to {model_output_dir}")


if __name__ == "__main__":
    train_finetuned_model()
