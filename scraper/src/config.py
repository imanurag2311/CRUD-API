"""Configuration and politeness settings for Books to Scrape pipeline.

Adheres to FlyRank Internship Week 5 (Assignment A9) politeness requirements:
- Honest User-Agent with repository contact link
- Minimum 500ms delay between live requests
- Strict request timeouts
- Disk caching for idempotency and reduced server load
"""
from pathlib import Path

# Target definitions (Sandbox practice site)
BASE_URL = "https://books.toscrape.com/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
ROBOTS_URL = "https://books.toscrape.com/robots.txt"
MAX_CATALOGUE_PAGES = 3
EXPECTED_RECORDS = 60

# Politeness rules
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/imanurag2311/CRUD-API)"
REQUEST_DELAY_SECONDS = 0.5   # At least 500ms between live network requests
REQUEST_TIMEOUT_SECONDS = 8.0 # Never hang forever on slow response
MAX_RETRIES = 1               # Single retry for 5xx or timeout; never retry 404/403

# Directory paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"

# Ensure output and cache directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
