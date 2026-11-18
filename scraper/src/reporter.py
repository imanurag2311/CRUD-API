"""Run Telemetry and Reporting for the polite scraper.

Stage 5 & Stage 6 deliverable:
Generates output/run-report.json with honest execution metrics:
- Start time, finish time, and duration
- Pages fetched, cache hits, live network calls
- Valid records count, invalid records count, and failed pages count
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from scraper.src.config import OUTPUT_DIR, BASE_URL, USER_AGENT, REQUEST_DELAY_SECONDS, REQUEST_TIMEOUT_SECONDS

class ScraperReporter:
    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = time.time()
        self.start_iso = datetime.now(timezone.utc).isoformat()
        
        self.catalogue_pages = 0
        self.detail_pages = 0
        self.cache_hits = 0
        self.live_requests = 0
        self.valid_records = 0
        self.invalid_records = 0
        self.failed_pages = 0
        self.failures: List[Dict[str, Any]] = []

    def record_failure(self, url: str, reason: str, status_code: int = 404):
        """Record a skipped / failed page for audit reporting."""
        self.failed_pages += 1
        self.failures.append({
            "url": url,
            "status_code": status_code,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def generate_report(self) -> Dict[str, Any]:
        """Compile and write output/run-report.json."""
        duration = round(time.time() - self.start_time, 2)
        
        report_data = {
            "timestamp": self.start_iso,
            "duration_seconds": duration,
            "catalogue_pages_crawled": self.catalogue_pages,
            "detail_pages_fetched": self.detail_pages,
            "cache_hits": self.cache_hits,
            "live_requests": self.live_requests,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "failed_pages": self.failed_pages,
            "target_site": BASE_URL,
            "politeness": {
                "user_agent": USER_AGENT,
                "min_delay_seconds": REQUEST_DELAY_SECONDS,
                "timeout_seconds": REQUEST_TIMEOUT_SECONDS,
                "caching_enabled": True
            },
            "failures": self.failures
        }

        report_path = self.output_dir / "run-report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        return report_data
