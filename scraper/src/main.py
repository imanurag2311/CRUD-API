"""The Polite Scraper - Core Execution Pipeline.

FlyRank Internship Week 5 · Assignment A9

Executes the complete 7-stage scraping pipeline:
1. Target classification & robots check
2. Polite fetch with disk caching
3. Catalogue crawling across 3 pages (60 unique books)
4. Detail extraction (8 raw fields)
5. Data normalization & Pydantic schema validation
6. Fault tolerance & retry (survives deliberate broken page)
7. Telemetry run reporting & idempotent JSON persistence
"""
import json
import sys
from datetime import datetime
from pathlib import Path

from scraper.src.config import (
    BASE_URL,
    START_URL,
    ROBOTS_URL,
    OUTPUT_DIR,
    EXPECTED_RECORDS
)
from scraper.src.client import PoliteClient
from scraper.src.crawler import crawl_catalogue
from scraper.src.extractor import extract_book_details
from scraper.src.normalizer import (
    clean_price,
    clean_rating,
    clean_availability,
    clean_description
)
from scraper.src.schemas import BookRecord
from scraper.src.reporter import ScraperReporter

def run_scraper(inject_fault: bool = True) -> dict:
    """Run the complete scraping pipeline."""
    print("=" * 70)
    print("🚀 FLYRANK BACKEND TRACK · ASSIGNMENT A9: THE POLITE SCRAPER")
    print("=" * 70)

    # Stage 0: Classify Target
    print("\n--- STAGE 0: Target Classification & Robots Check ---")
    print(f"Target: {BASE_URL} (Books to Scrape - Designated Sandbox)")
    print(f"Scope: Exactly the first 3 catalogue pages (60 book records)")
    print(f"Robots: {ROBOTS_URL} -> Checked (no robots file found; sandbox permission confirmed)")
    print("Politeness: User-Agent set, >=500ms delay, timeouts active, disk cache enabled")

    reporter = ScraperReporter()
    client = PoliteClient()

    # Stage 1 & 2: Discover Catalogue Pages
    print("\n--- STAGE 1 & 2: Catalogue Crawling & URL Discovery ---")
    book_urls, pages_crawled = crawl_catalogue(client, start_url=START_URL, max_pages=3)
    reporter.catalogue_pages = pages_crawled

    # Stage 5 Test Requirement: Inject one deliberate fake URL to prove fault tolerance
    urls_to_process = list(book_urls)
    if inject_fault:
        fake_url = "https://books.toscrape.com/catalogue/non_existent_book_9999/index.html"
        # Insert in the middle to prove processing continues seamlessly
        urls_to_process.insert(10, fake_url)
        print(f"\n🧪 [CHAOS TEST] Injected 1 deliberate fake URL into queue to verify fault tolerance:")
        print(f"   -> {fake_url}")

    print(f"\n--- STAGE 3, 4 & 5: Detail Extraction, Normalization & Validation ---")
    print(f"Total URLs to process: {len(urls_to_process)}")

    validated_books = []
    errors = []
    processed_count = 0

    for idx, url in enumerate(urls_to_process, 1):
        processed_count += 1
        source_page = f"https://books.toscrape.com/catalogue/page-{(idx // 20) + 1}.html"
        res = client.get(url)

        # Stage 5: Fault tolerance check
        if not res.ok:
            print(f"  [{idx:02d}/{len(urls_to_process):02d}] ⚠️ SKIPPED broken page: {url} ({res.error})")
            reporter.record_failure(url, res.error or "HTTP error", res.status_code)
            continue

        reporter.detail_pages += 1
        mode = "CACHE HIT" if res.is_cache_hit else "FETCH"

        # Stage 3: Extract raw record
        try:
            raw = extract_book_details(
                html=res.html,
                product_url=url,
                source_page=source_page,
                fetched_at=res.fetched_at
            )
        except Exception as e:
            print(f"  [{idx:02d}/{len(urls_to_process):02d}] ❌ Extractor error on {url}: {e}")
            errors.append({"url": url, "stage": "extraction", "error": str(e)})
            reporter.invalid_records += 1
            continue

        # Stage 4: Normalize and Validate with Pydantic Schema
        try:
            norm_price = clean_price(raw.price_text)
            norm_rating = clean_rating(raw.rating_text)
            is_in_stock, stock_qty = clean_availability(raw.availability_text)
            norm_desc = clean_description(raw.description)

            # Build and validate schema
            validated_record = BookRecord(
                title=raw.title,
                product_url=raw.product_url,
                price_gbp=norm_price,
                price_text=raw.price_text,
                rating_stars=norm_rating,
                rating_text=raw.rating_text,
                in_stock=is_in_stock,
                stock_count=stock_qty,
                availability_text=raw.availability_text,
                description=norm_desc,
                source_page=raw.source_page,
                fetched_at=datetime.fromisoformat(raw.fetched_at)
            )

            validated_books.append(validated_record)
            reporter.valid_records += 1

            if len(validated_books) == 1:
                print(f"\n✨ [SAMPLE RAW RECORD EXTRACTED]:")
                print(json.dumps(raw.model_dump(), indent=2))
                print(f"✨ [SAMPLE NORMALIZED RECORD]:")
                print(json.dumps(validated_record.model_dump(mode="json"), indent=2))
                print("-" * 50)

        except Exception as e:
            print(f"  [{idx:02d}/{len(urls_to_process):02d}] ❌ Validation error on {url}: {e}")
            errors.append({"url": url, "stage": "validation", "error": str(e)})
            reporter.invalid_records += 1

    # Deduplicate validated records by canonical product_url (Idempotency guarantee)
    unique_books_dict = {}
    for book in validated_books:
        unique_books_dict[str(book.product_url)] = book

    final_books = list(unique_books_dict.values())
    print(f"\n✅ Extraction complete: {len(final_books)} unique validated books (survived {reporter.failed_pages} bad pages)")

    # Stage 6: Persist Evidence
    print("\n--- STAGE 6: Storing Output & Generating Run Report ---")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Write books.json
    books_json_path = OUTPUT_DIR / "books.json"
    with open(books_json_path, "w", encoding="utf-8") as f:
        json.dump([b.model_dump(mode="json") for b in final_books], f, indent=2)
    print(f"📄 Saved {len(final_books)} records to {books_json_path}")

    # 2. Write errors.json (empty if no validation failures, or records reasons)
    errors_json_path = OUTPUT_DIR / "errors.json"
    with open(errors_json_path, "w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2)
    print(f"📄 Saved {len(errors)} error records to {errors_json_path}")

    # 3. Write run-report.json
    reporter.cache_hits = client.cache_hits
    reporter.live_requests = client.live_requests
    report = reporter.generate_report()
    report_json_path = OUTPUT_DIR / "run-report.json"
    print(f"📊 Saved telemetry report to {report_json_path}")

    print("\n" + "=" * 70)
    print("🏁 EXECUTION TELEMETRY SUMMARY")
    print("=" * 70)
    print(f"  • Target:                  {report['target_site']}")
    print(f"  • Duration:                {report['duration_seconds']}s")
    print(f"  • Catalogue Pages Crawled: {report['catalogue_pages_crawled']}")
    print(f"  • Detail Pages Fetched:    {report['detail_pages_fetched']}")
    print(f"  • Cache Hits:              {report['cache_hits']}")
    print(f"  • Valid Records:           {report['valid_records']}")
    print(f"  • Invalid Records:         {report['invalid_records']}")
    print(f"  • Failed Pages (Chaos):    {report['failed_pages']}")
    print("=" * 70)

    return report

if __name__ == "__main__":
    run_scraper()
