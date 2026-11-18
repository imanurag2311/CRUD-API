"""Pydantic schemas for the polite scraper pipeline.

Stage 3 & Stage 4 deliverables:
- RawBookRecord: Captures raw string representations from HTML + provenance
- BookRecord: Strongly typed, validated model for persistent JSON storage
- RunReport: Execution telemetry and audit metrics
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, ConfigDict

class RawBookRecord(BaseModel):
    """Raw record directly extracted from book detail HTML."""
    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str

class BookRecord(BaseModel):
    """Normalized, schema-validated record written to output/books.json."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, description="Book title")
    product_url: HttpUrl = Field(description="Canonical absolute URL of the product page")
    price_gbp: float = Field(gt=0.0, description="Normalized price in GBP")
    price_text: str = Field(description="Original price text with currency symbol")
    rating_stars: int = Field(ge=1, le=5, description="Star rating converted to integer 1-5")
    rating_text: str = Field(description="Original rating textual representation")
    in_stock: bool = Field(description="True if product is currently available")
    stock_count: int = Field(ge=0, description="Quantity available in stock")
    availability_text: str = Field(description="Original availability string")
    description: Optional[str] = Field(default=None, description="Book description or null")
    source_page: HttpUrl = Field(description="Catalogue page where link was discovered")
    fetched_at: datetime = Field(description="ISO-8601 UTC timestamp of fetch")

class RunReport(BaseModel):
    """Execution telemetry written to output/run-report.json."""
    timestamp: str
    duration_seconds: float
    catalogue_pages_crawled: int
    detail_pages_fetched: int
    cache_hits: int
    live_requests: int
    valid_records: int
    invalid_records: int
    failed_pages: int
    target_site: str
    politeness: dict
