import pandas as pd

results = [
    {
        "Model": "XLM-R Claim Only",
        "Accuracy": 0.6301,
        "Macro_F1": 0.5892,
    },
    {
        "Model": "AfriBERTa Claim Only",
        "Accuracy": 0.5711,
        "Macro_F1": 0.5687,
    },
    {
        "Model": "XLM-R Gold Evidence",
        "Accuracy": 0.6301,
        "Macro_F1": 0.5892,
    },
    {
        "Model": "AfriBERTa Gold Evidence",
        "Accuracy": 0.5711,
        "Macro_F1": 0.5687,
    },
    {
        "Model": "Qwen Claim Only",
        "Accuracy": 0.3902,
        "Macro_F1": 0.3807,
    },
    {
        "Model": "Qwen Gold Evidence",
        "Accuracy": 0.4593,
        "Macro_F1": 0.4004,
    },
    {
        "Model": "Qwen Gold Evidence + Reasoning",
        "Accuracy": 0.4370,
        "Macro_F1": 0.4252,
    },
    {
        "Model": "Qwen BM25 Evidence",
        "Accuracy": 0.3943,
        "Macro_F1": 0.3182,
    },
]

df = pd.DataFrame(results)

print("\nFINAL EXPERIMENT SUMMARY\n")
print(df)

print("\nSORTED BY ACCURACY\n")
print(df.sort_values("Accuracy", ascending=False))

df.to_csv(
    "results/final_experiment_summary.csv",
    index=False,
)

print(
    "\nSaved to results/final_experiment_summary.csv"
)