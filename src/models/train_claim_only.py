from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
MODEL_NAME = "xlm-roberta-base"
LABEL2ID = {
    "supports": 0,
    "refutes": 1,
    "nei": 2
}

ID2LABEL = {
    0: "supports",
    1: "refutes",
    2: "nei"
}
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="macro"
    )

    accuracy = accuracy_score(labels, predictions)

    return {
        "accuracy": accuracy,
        "macro_f1": f1,
        "precision": precision,
        "recall": recall
    }

def preprocess_function(examples):
    return tokenizer(
        examples["claim"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

def main():

    dataset = load_dataset(
        "json",
        data_files="data/processed/afrifact_nigerian_languages.jsonl"
    )

    dataset = dataset["train"]

    train_dataset = dataset.filter(lambda x: x["split"] == "train")
    val_dataset = dataset.filter(lambda x: x["split"] == "validation")
    test_dataset = dataset.filter(lambda x: x["split"] == "test")
    train_dataset = train_dataset.map(
        lambda x: {"label": LABEL2ID[x["label"]]}
    )

    val_dataset = val_dataset.map(
        lambda x: {"label": LABEL2ID[x["label"]]}
    )

    test_dataset = test_dataset.map(
        lambda x: {"label": LABEL2ID[x["label"]]}
    )

    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = train_dataset.map(preprocess_function, batched=True)
    val_dataset = val_dataset.map(preprocess_function, batched=True)
    test_dataset = test_dataset.map(preprocess_function, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    training_args = TrainingArguments(
        output_dir="outputs/xlmr_claim_only",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        fp16=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    trainer.train()

    results = trainer.evaluate(test_dataset)
    print("\nTEST RESULTS")
    print(results)


if __name__ == "__main__":
    main()