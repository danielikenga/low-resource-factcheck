import json
import os
import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

MODEL_NAME = "xlm-roberta-base"

LABEL2ID = {"supports": 0, "refutes": 1, "nei": 2}
ID2LABEL = {0: "supports", 1: "refutes", 2: "nei"}


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="macro", zero_division=0
    )
    accuracy = accuracy_score(labels, predictions)

    return {
        "accuracy": accuracy,
        "macro_f1": f1,
        "precision": precision,
        "recall": recall,
    }


def preprocess_function(examples):
    return tokenizer(
        examples["claim"],
        truncation=True,
        padding="max_length",
        max_length=128,
    )


def load_split(df, split_name):
    split_df = df[df["split"] == split_name].copy()
    split_df["label"] = split_df["label"].map(LABEL2ID)

    split_df = split_df[["claim", "label", "language"]]
    return Dataset.from_pandas(split_df, preserve_index=False)


def main():
    df = pd.read_json(
        "data/processed/afrifact_nigerian_languages.jsonl",
        lines=True,
    )

    train_dataset = load_split(df, "train")
    val_dataset = load_split(df, "validation")
    test_dataset = load_split(df, "test")

    print("Train:", len(train_dataset))
    print("Validation:", len(val_dataset))
    print("Test:", len(test_dataset))

    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = train_dataset.map(preprocess_function, batched=True)
    val_dataset = val_dataset.map(preprocess_function, batched=True)
    test_dataset = test_dataset.map(preprocess_function, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    training_args = TrainingArguments(
        output_dir="outputs/xlmr_claim_only",
        eval_strategy="epoch",
        save_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_dir="outputs/logs",
        load_best_model_at_end=False,
        fp16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    results = trainer.evaluate(test_dataset)

    print("\n TEST RESULTS ")
    print(results)

    os.makedirs("results/baselines", exist_ok=True)

    with open("results/baselines/xlmr_claim_only_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\nSaved the results to results/baselines/xlmr_claim_only_results.json")


if __name__ == "__main__":
    main()