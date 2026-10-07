# ✈️ RRG Daily Flight Scraper

An automated daily web scraper designed to track and extract flight departure details from the Mauritius Airport (ATOL) portal, specifically focusing on flights to and from Rodrigues.

## 🚀 Overview

This repository runs an automated GitHub Actions workflow every day to fetch the latest flight schedules, filter out relevant Rodrigues flight numbers (handling partner codes like MK correctly), and generate clean daily text logs (`flights_YYYY-MM-DD.txt`) formatted for CSPro data entry.

## ⚙️ How It Works

1. **Automation Schedule:** Triggered daily via GitHub Actions cron schedule (`0 19 * * *` UTC / `23:00` Mauritius Time) or manually via `workflow_dispatch`.
2. **Scraper Script (`scraper.py`):** 
   - Utilizes **SeleniumBase** (`uc=True` mode) in a headless browser environment to successfully bypass anti-bot challenges (such as Cloudflare).
   - Scans pagination pages from the ATOL flight departure portal.
   - Filters rows mentioning "Rodrigues" and extracts valid flight designators.
3. **Data Storage:** Automatically commits and pushes the generated `flights_YYYY-MM-DD.txt` log back into the repository.

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Automation:** GitHub Actions
* **Scraping Engine:** SeleniumBase
* **Output Format:** Plain Text / CSPro compatible logs

## 📁 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions workflow configuration
├── scraper.py              # Core Python scraping script
└── flights_*.txt           # Auto-generated daily flight log outputs
