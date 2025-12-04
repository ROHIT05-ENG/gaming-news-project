import requests
from bs4 import BeautifulSoup
import yaml
import csv
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCES_PATH = os.path.join(BASE_DIR, "src", "indexer", "evidence_sources.yaml")
OUT_RAW = os.path.join(BASE_DIR, "data", "evidence", "evidence_raw.csv")

def load_sources():
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("sources", [])

def crawl_rss(url):
    print(f"Crawling: {url}")
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        print("  Failed:", e)
        return []

    soup = BeautifulSoup(resp.text, "xml")
    items = soup.find_all("item")
    articles = []
    for item in items:
        title = item.find("title").get_text(strip=True) if item.find("title") else ""
        # description may contain HTML or CDATA; extract text
        desc = item.find("description")
        text = desc.get_text(strip=True) if desc else ""
        articles.append([title, text])
    return articles

def save_raw(rows):
    os.makedirs(os.path.dirname(OUT_RAW), exist_ok=True)
    with open(OUT_RAW, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "text", "scraped_at"])
        now = datetime.utcnow().isoformat()
        for r in rows:
            writer.writerow([r[0], r[1], now])
    print("Saved raw CSV:", OUT_RAW)

def main():
    sources = load_sources()
    all_articles = []
    for src in sources:
        url = src.get("url")
        if not url:
            continue
        articles = crawl_rss(url)
        all_articles.extend(articles)

    # deduplicate by title (simple)
    seen = set()
    unique = []
    for t, body in all_articles:
        key = (t or "").strip()
        if key and key not in seen:
            seen.add(key)
            unique.append([t, body])
    save_raw(unique)
    print("Crawling finished. Articles:", len(unique))

if __name__ == "__main__":
    main()
