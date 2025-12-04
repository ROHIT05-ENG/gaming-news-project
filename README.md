# Gaming Evidence Collector (Team B)

This repo collects gaming news from selected RSS feeds, cleans them, and stores:
- `data/evidence/evidence_raw.csv`
- `data/evidence/evidence_clean.csv`

The repository is configured to run the crawler and cleaner daily using GitHub Actions.

## Local run (dev)

1. Create virtualenv and activate:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
