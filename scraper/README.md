# 🕷️ Assignment A9: The Polite Scraper

A robust, ethical, and schema-validated web scraping pipeline engineered with **Python**, **Requests**, **BeautifulSoup4**, and **Pydantic**. Built as part of the **FlyRank.ai AI Backend Engineering Track (Week 5 · Assignment A9)**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green?style=for-the-badge)](https://www.crummy.com/software/BeautifulSoup/)
[![Pytest](https://img.shields.io/badge/Pytest-Passing%20(8%2F8)-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## 🎯 Target Classification & Ethical Permission

* **Target Site:** [`https://books.toscrape.com/`](https://books.toscrape.com/)
* **Purpose & Permission:** Books to Scrape is an official, public sandbox specifically designed and hosted for students and engineers to practise automated scraping without legal or operational hazards. That explicit declaration on the homepage is our permission.
* **Robots.txt Check:**
  - Endpoint queried: `https://books.toscrape.com/robots.txt`
  - Observation: **No robots file found (HTTP 404)**. As taught in the engineering guidelines, a missing `robots.txt` file is not an open permission to hammer a site; it simply means no machine-readable exclusion file was placed.
* **Scope Definition:** Scrapes **strictly the first 3 catalogue pages** (`page-1.html` to `page-3.html`), discovering and parsing exactly **60 unique book detail pages**.
* **Mandatory Ethics Declaration:**
  > *"I will not reuse this code on another site without checking its rules, terms of service, and robots.txt first."*

---

## 🛡️ Politeness Rules & Engineering Habits

This scraper implements the five professional habits of ethical data collection:

| Politeness Habit | Technical Implementation | Why It Matters |
| :--- | :--- | :--- |
| **Honest Identification** | `User-Agent: FlyRankInternship-A9/1.0 (+https://github.com/imanurag2311/CRUD-API)` | Site administrators can identify the automated client and reach the author if needed. |
| **Rate Limiting** | Strict `time.sleep` enforcing $\ge 500\text{ ms}$ between live requests | Prevents denial-of-service spikes and respects target server capacity. |
| **Request Timeout** | `timeout = 8.0` seconds on all HTTP requests | Prevents pipeline hanging indefinitely on slow or stalled network sockets. |
| **Two-Tier Disk Cache** | Hashes URLs to `cache/*.html` with local hit detection | During development and re-runs, requests hit local disk with 0 network load. |
| **Status Verification** | Only `200 OK` proceeds to parser; `404` & `403` are skipped without retry | A polite robot never hammers a missing page or ignores an explicit refusal. |

---

## 📑 Record Schema & Architecture

The scraper separates untrusted raw text extraction from strongly-typed normalized records using **Pydantic**:

```
Messy HTML String ───► BeautifulSoup ───► RawBookRecord (Strings) ───► Normalizer ───► BookRecord (Pydantic Schema) ───► books.json
```

### Validated Record Schema (`BookRecord`):

| Field | Type | Validation / Description |
| :--- | :---: | :--- |
| `title` | `str` | Book title (non-empty string). |
| `product_url` | `HttpUrl` | Canonical absolute URL (e.g. `https://books.toscrape.com/catalogue/...`). |
| `price_gbp` | `float` | Cleaned positive float parsed from price text (e.g. `51.77`). |
| `price_text` | `str` | Raw original text including currency symbol (e.g. `"£51.77"`). |
| `rating_stars` | `int` | Normalized star rating between 1 and 5 (from `"Three"` $\to$ `3`). |
| `rating_text` | `str` | Raw star rating class name (e.g. `"Three"`). |
| `in_stock` | `bool` | Boolean flag indicating product availability. |
| `stock_count` | `int` | Integer parsed from stock text (e.g. `22` from `"In stock (22 available)"`). |
| `availability_text` | `str` | Raw availability string. |
| `description` | `Optional[str]` | Cleaned description text, or `null` if missing (never fabricated). |
| `source_page` | `HttpUrl` | Provenance receipt: the catalogue URL where the book link was discovered. |
| `fetched_at` | `datetime` | Provenance receipt: ISO-8601 UTC timestamp of the fetch. |

---

## ⚡ Quickstart & How to Run

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 pydantic pytest
```

### 2. Execute the Pipeline
Run the scraper from the repository root:
```bash
python -m scraper.src.main
```

### 3. Run Automated Unit Tests
```bash
python -m pytest scraper/tests/ -v
```

---

## 📊 Real Execution Telemetry Proof (`output/run-report.json`)

The following is the actual telemetry report output by the pipeline:

```json
{
  "timestamp": "2026-11-16T03:19:28.703688+00:00",
  "duration_seconds": 0.23,
  "catalogue_pages_crawled": 3,
  "detail_pages_fetched": 60,
  "cache_hits": 63,
  "live_requests": 0,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1,
  "target_site": "https://books.toscrape.com/",
  "politeness": {
    "user_agent": "FlyRankInternship-A9/1.0 (+https://github.com/imanurag2311/CRUD-API)",
    "min_delay_seconds": 0.5,
    "timeout_seconds": 8.0,
    "caching_enabled": true
  },
  "failures": [
    {
      "url": "https://books.toscrape.com/catalogue/non_existent_book_9999/index.html",
      "status_code": 404,
      "reason": "HTTP 404: Not Found",
      "timestamp": "2026-11-16T03:19:28.810997+00:00"
    }
  ]
}
```

---

## 🧪 Fault Tolerance & Chaos Testing (Stage 5)

To prove that the scraper handles errors gracefully without crashing the entire run:
1. One deliberate fake URL (`https://books.toscrape.com/catalogue/non_existent_book_9999/index.html`) is injected into the queue.
2. The client catches the `404 Not Found` response.
3. The polite robot rule triggers: it **refuses to retry 404s** (re-knocking on a non-existent door is pointless and annoying).
4. The failure is recorded in `output/run-report.json` under `"failures"`, and the run continues.
5. All **60 valid books** survive into `output/books.json`.

---

## 🌐 Browser Cost Comparison Note

> **Why this assignment needed no browser:**  
> The target website serves clean, server-side rendered (`SSR`) HTML. All data—titles, prices, ratings, and descriptions—is fully present in the initial HTTP response body.  
> Using a headless browser (Playwright, Puppeteer, or Selenium) would launch a full Chromium instance, consuming **~300 MB of RAM** and taking **several seconds per page** to evaluate JavaScript that doesn't exist. In contrast, `requests` + `BeautifulSoup` requires **< 15 MB of RAM** and parses each document in **under 5 milliseconds**, making it 100x faster, cheaper, and more sustainable.

---

## ⚖️ Ownership & License

**Copyright © 2026 Anurag Yadav. All Rights Reserved.**  
Developed for the FlyRank.ai AI Backend Engineering Internship.
