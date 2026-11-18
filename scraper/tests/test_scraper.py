"""Unit tests for the polite scraper pipeline.

Deliverable (Section 7 - Done means):
At least five unit tests:
1. Price normalization
2. Relative -> Absolute URLs
3. Missing description handling (returns None)
4. Duplicate URL deduplication
5. Malformed HTML fixture handling
6. Rating conversion
7. Availability & stock parsing
8. Pydantic schema validation & error rejection
"""
import pytest
from pathlib import Path
from pydantic import ValidationError

from scraper.src.normalizer import (
    clean_price,
    clean_rating,
    clean_availability,
    to_absolute_url,
    clean_description
)
from scraper.src.extractor import extract_book_details, extract_catalogue_links
from scraper.src.schemas import BookRecord
from scraper.src.config import FIXTURES_DIR

# 1. Price normalization test
def test_price_normalization():
    assert clean_price("£51.77") == 51.77
    assert clean_price("£10.00") == 10.0
    assert clean_price("99.95") == 99.95
    with pytest.raises(ValueError):
        clean_price("")
    with pytest.raises(ValueError):
        clean_price("£0.00")
    with pytest.raises(ValueError):
        clean_price("free")

# 2. Rating conversion test
def test_rating_conversion():
    assert clean_rating("One") == 1
    assert clean_rating("Two") == 2
    assert clean_rating("Three") == 3
    assert clean_rating("Four") == 4
    assert clean_rating("Five") == 5
    with pytest.raises(ValueError):
        clean_rating("Six")
    with pytest.raises(ValueError):
        clean_rating("")

# 3. Availability and stock count parsing test
def test_availability_parsing():
    in_stock, qty = clean_availability("In stock (22 available)")
    assert in_stock is True
    assert qty == 22

    in_stock, qty = clean_availability("In stock (1 available)")
    assert in_stock is True
    assert qty == 1

    in_stock, qty = clean_availability("In stock")
    assert in_stock is True
    assert qty == 1

    in_stock, qty = clean_availability("Out of stock")
    assert in_stock is False
    assert qty == 0

# 4. Relative to absolute URL resolution test
def test_relative_to_absolute_url():
    base = "https://books.toscrape.com/catalogue/page-1.html"
    rel = "a-light-in-the-attic_1000/index.html"
    abs_url = to_absolute_url(base, rel)
    assert abs_url == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    parent_rel = "../tipping-the-velvet_999/index.html"
    abs_parent = to_absolute_url(base, parent_rel)
    assert abs_parent == "https://books.toscrape.com/tipping-the-velvet_999/index.html"

# 5. Missing description handling (returns None)
def test_missing_description_from_fixture():
    fixture_path = FIXTURES_DIR / "book_no_desc.html"
    assert fixture_path.exists(), "Missing fixture file book_no_desc.html"
    html = fixture_path.read_text(encoding="utf-8")

    raw = extract_book_details(
        html=html,
        product_url="https://books.toscrape.com/catalogue/test-book-no-desc/index.html",
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-11-16T08:00:00Z"
    )
    assert raw.description is None
    assert clean_description(raw.description) is None

# 6. Malformed HTML fixture test
def test_malformed_html_fixture():
    fixture_path = FIXTURES_DIR / "book_malformed.html"
    assert fixture_path.exists(), "Missing fixture file book_malformed.html"
    html = fixture_path.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="Could not locate 'article.product_page'"):
        extract_book_details(
            html=html,
            product_url="https://books.toscrape.com/catalogue/broken/index.html",
            source_page="https://books.toscrape.com/catalogue/page-1.html",
            fetched_at="2026-11-16T08:00:00Z"
        )

# 7. Valid book detail extraction test
def test_valid_book_extraction():
    fixture_path = FIXTURES_DIR / "book_valid.html"
    assert fixture_path.exists(), "Missing fixture file book_valid.html"
    html = fixture_path.read_text(encoding="utf-8")

    raw = extract_book_details(
        html=html,
        product_url="https://books.toscrape.com/catalogue/test-book/index.html",
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-11-16T08:00:00Z"
    )
    assert raw.title == "Test Book Title"
    assert raw.price_text == "£25.50"
    assert raw.rating_text == "Four"
    assert raw.availability_text == "In stock (10 available)"
    assert raw.description == "A test description."

# 8. Pydantic schema validation test
def test_pydantic_schema_validation():
    # Valid record
    valid = BookRecord(
        title="Valid Book",
        product_url="https://books.toscrape.com/catalogue/valid/index.html",
        price_gbp=19.99,
        price_text="£19.99",
        rating_stars=4,
        rating_text="Four",
        in_stock=True,
        stock_count=5,
        availability_text="In stock (5 available)",
        description="A book description",
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-11-16T08:00:00Z"
    )
    assert valid.price_gbp == 19.99
    assert valid.rating_stars == 4

    # Invalid price (negative)
    with pytest.raises(ValidationError):
        BookRecord(
            title="Bad Price Book",
            product_url="https://books.toscrape.com/catalogue/bad/index.html",
            price_gbp=-5.0, # Negative not allowed
            price_text="£-5.00",
            rating_stars=3,
            rating_text="Three",
            in_stock=True,
            stock_count=1,
            availability_text="In stock",
            source_page="https://books.toscrape.com/catalogue/page-1.html",
            fetched_at="2026-11-16T08:00:00Z"
        )

    # Invalid rating (out of bounds)
    with pytest.raises(ValidationError):
        BookRecord(
            title="Bad Rating Book",
            product_url="https://books.toscrape.com/catalogue/bad/index.html",
            price_gbp=10.0,
            price_text="£10.00",
            rating_stars=7, # Must be between 1 and 5
            rating_text="Seven",
            in_stock=True,
            stock_count=1,
            availability_text="In stock",
            source_page="https://books.toscrape.com/catalogue/page-1.html",
            fetched_at="2026-11-16T08:00:00Z"
        )
