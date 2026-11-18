"""Catalogue Crawler for Books to Scrape.

Discovers the first 3 catalogue pages by following pagination links:
- Page 1 -> Page 2 -> Page 3
- Discovers exactly 60 unique book detail URLs (20 books per page)
- Deduplicates URLs before passing to detail extractor
"""
from typing import List, Tuple
from scraper.src.client import PoliteClient
from scraper.src.extractor import extract_catalogue_links
from scraper.src.config import START_URL, MAX_CATALOGUE_PAGES

def crawl_catalogue(client: PoliteClient, start_url: str = START_URL, max_pages: int = MAX_CATALOGUE_PAGES) -> Tuple[List[str], int]:
    """Crawl the first N catalogue pages and return deduplicated book detail URLs."""
    current_url = start_url
    discovered_urls: List[str] = []
    pages_crawled = 0

    print(f"🔍 Starting catalogue crawl at: {start_url}")

    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        res = client.get(current_url)
        if not res.ok:
            raise RuntimeError(f"Failed to fetch catalogue page {pages_crawled} ({current_url}): {res.error}")

        mode = "CACHE HIT" if res.is_cache_hit else "FETCH"
        print(f"  [{mode}] Catalogue Page {pages_crawled}: {current_url} ({len(res.html)} bytes)")

        # Extract book links & next page link
        book_links, next_url = extract_catalogue_links(res.html, current_url)
        discovered_urls.extend(book_links)
        
        current_url = next_url

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for u in discovered_urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    print(f"✅ Catalogue crawl complete: catalogue_pages={pages_crawled}, discovered={len(discovered_urls)}, unique_urls={len(unique_urls)}")
    return unique_urls, pages_crawled
