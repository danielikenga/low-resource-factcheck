import os
import re
import pandas as pd
from rank_bm25 import BM25Okapi


DATA_PATH = "data/processed/afrifact_nigerian_languages_custom_split.jsonl"
OUTPUT_PATH = "results/retrieval/bm25_retrieved_evidence.csv"


def tokenize(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.split()


def main():
    os.makedirs("results/retrieval", exist_ok=True)

    df = pd.read_json(DATA_PATH, lines=True)

    corpus_df = df.copy()
    corpus_df["extracted_evidence_text"] = (
        corpus_df["extracted_evidence_text"]
        .fillna("")
        .astype(str)
    )

    corpus_texts = corpus_df["extracted_evidence_text"].tolist()
    tokenized_corpus = [tokenize(text) for text in corpus_texts]

    bm25 = BM25Okapi(tokenized_corpus)

    test_df = df[df["split"] == "custom_test"].copy()

    results = []

    for i, row in test_df.iterrows():
        claim = str(row["claim"])
        tokenized_query = tokenize(claim)

        scores = bm25.get_scores(tokenized_query)
        top_idx = scores.argmax()

        retrieved_row = corpus_df.iloc[top_idx]

        correct_source = row["id"] == retrieved_row["id"]

        results.append({
            "query_id": row["id"],
            "language": row["language"],
            "claim": claim,
            "gold_label": row["label"],
            "gold_evidence": row["extracted_evidence_text"],
            "retrieved_id": retrieved_row["id"],
            "retrieved_language": retrieved_row["language"],
            "retrieved_evidence": retrieved_row["extracted_evidence_text"],
            "bm25_score": scores[top_idx],
            "retrieved_exact_gold": correct_source,
        })

        print(
            f"{len(results)}/{len(test_df)} | "
            f"lang={row['language']} | "
            f"match={correct_source} | "
            f"score={scores[top_idx]:.4f}"
        )

    result_df = pd.DataFrame(results)

    print("\nBM25 RETRIEVAL RESULTS")
    print("Total:", len(result_df))
    print("Exact gold evidence retrieved:")
    print(result_df["retrieved_exact_gold"].mean())

    print("\nBy language:")
    print(result_df.groupby("language")["retrieved_exact_gold"].mean())

    result_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved BM25 retrieved evidence to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()