import csv
import os
import html
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IN_RAW = os.path.join(BASE_DIR, "data", "evidence", "evidence_raw.csv")
OUT_CLEAN = os.path.join(BASE_DIR, "data", "evidence", "evidence_clean.csv")

def clean_text(text):
    if not text:
        return ""
    # unescape HTML entities
    text = html.unescape(text)
    # remove html tags if any (simple)
    text = re.sub(r"<[^>]+>", " ", text)
    # normalize whitespace
    text = " ".join(text.split())
    return text.strip()

def main():
    if not os.path.exists(IN_RAW):
        print("Raw file not found:", IN_RAW)
        return

    rows = []
    with open(IN_RAW, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            title = clean_text(r.get("title", ""))
            text = clean_text(r.get("text", ""))
            if not title and not text:
                continue
            rows.append([title, text])

    os.makedirs(os.path.dirname(OUT_CLEAN), exist_ok=True)
    with open(OUT_CLEAN, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "text"])
        writer.writerows(rows)

    print("Cleaned file written:", OUT_CLEAN, "rows:", len(rows))

if __name__ == "__main__":
    main()
