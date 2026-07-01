import json
import os
import pandas as pd

RESULTS_DIR = "results"

rows = []

for root, _, files in os.walk(RESULTS_DIR):

    for file in files:

        if not file.endswith("_results.json"):
            continue

        path = os.path.join(root, file)

        with open(path) as f:
            result = json.load(f)

        rows.append({

            "Experiment": file.replace("_results.json", ""),

            "Accuracy": result.get("accuracy"),

            "Macro_F1": result.get("macro_f1"),

            "Precision": result.get("precision"),

            "Recall": result.get("recall"),

            "Valid Predictions": result.get("valid_predictions")

        })

df = pd.DataFrame(rows)

df = df.sort_values("Experiment")

os.makedirs("results/analysis", exist_ok=True)

df.to_csv(
    "results/analysis/master_results.csv",
    index=False
)

print(df)

print("\nSaved to results/analysis/master_results.csv")