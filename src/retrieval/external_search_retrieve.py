import os
import time
import urllib.parse
import pandas as pd
import requests
from bs4 import BeautifulSoup


DATA_PATH = "data/processed/afrifact_nigerian_languages_custom_split.jsonl"
OUTPUT_PATH = "results/retrieval/external_search_results.csv"

TRUSTED_SITES = [
    "bbc.com",
    "dubawa.org",
    "africacheck.org",
    "factcheckhub.com",
    "channelstv.com",
    "arisetvnews.com",
]

LIMIT = 10


def search_duckduckgo(query, max_results=5):
    url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select(".result"):
        title_tag = result.select_one(".result__title")
        link_tag = result.select_one(".result__a")
        snippet_tag = result.select_one(".result__snippet")

        if not link_tag:
            continue

        title = title_tag.get_text(" ", strip=True) if title_tag else ""
        link = link_tag.get("href", "")
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

        results.append({
            "title": title,
            "url": link,
            "snippet": snippet,
        })

        if len(results) >= max_results:
            break

    return results


def build_external_query(claim):
    site_filter = " OR ".join([f"site:{site}" for site in TRUSTED_SITES])
    return f"{claim} ({site_filter})"


def main():
    os.makedirs("results/retrieval", exist_ok=True)

    df = pd.read_json(DATA_PATH, lines=True)
    test_df = df[df["split"] == "custom_test"].copy().head(LIMIT)

    rows = []

    for count, (_, row) in enumerate(test_df.iterrows(), start=1):
        claim = str(row["claim"])
        query = build_external_query(claim)

        print(f"\n{count}/{len(test_df)}")
        print("CLAIM:", claim[:200])
        print("QUERY:", query[:250])

        try:
            search_results = search_duckduckgo(query, max_results=5)
        except Exception as e:
            print("SEARCH ERROR:", e)
            search_results = []

        if not search_results:
            rows.append({
                "id": row["id"],
                "language": row["language"],
                "claim": claim,
                "gold_label": row["label"],
                "rank": None,
                "title": "",
                "url": "",
                "snippet": "",
                "retrieved_text": "",
            })
            continue

        for rank, result in enumerate(search_results, start=1):
            retrieved_text = f"{result['title']} {result['snippet']}"

            rows.append({
                "id": row["id"],
                "language": row["language"],
                "claim": claim,
                "gold_label": row["label"],
                "rank": rank,
                "title": result["title"],
                "url": result["url"],
                "snippet": result["snippet"],
                "retrieved_text": retrieved_text,
            })

            print(f"Rank {rank}: {result['title'][:100]}")

        time.sleep(2)

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved external search results to {OUTPUT_PATH}")
    print("Rows:", len(out_df))


if __name__ == "__main__":
    main()