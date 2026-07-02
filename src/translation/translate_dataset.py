import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
import os

INPUT_PATH = "data/processed/afrifact_nigerian_languages_custom_split.jsonl"
OUTPUT_PATH = "data/processed/afrifact_translated_test.jsonl"


def translate_text(text):

    if pd.isna(text):
        return ""

    text = str(text).strip()

    if text == "":
        return ""

    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        print("Translation failed:", e)
        return text


def main():

    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_json(INPUT_PATH, lines=True)

    test_df = df[df["split"] == "custom_test"].copy()
    #test_df = test_df.head(5) (testing translation is stable with 5)

    print(f"Translating {len(test_df)} examples...")

    translated_claims = []
    translated_evidence = []

    for _, row in tqdm(test_df.iterrows(), total=len(test_df)):

        translated_claims.append(
            translate_text(row["claim"])
        )

        translated_evidence.append(
            translate_text(row["extracted_evidence_text"])
        )

    test_df["translated_claim"] = translated_claims
    test_df["translated_evidence"] = translated_evidence

    test_df.to_json(
        OUTPUT_PATH,
        orient="records",
        lines=True,
        force_ascii=False
    )

    print("\nSaved translated dataset to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()