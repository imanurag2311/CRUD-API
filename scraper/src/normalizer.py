"""Data normalization functions for Books to Scrape HTML fields.

Transforms raw text into clean, typed Python values:
- "£51.77" -> 51.77 (float)
- "Three" -> 3 (int)
- "In stock (22 available)" -> True, 22
- Relative URLs -> Absolute canonical URLs
"""
import re
from typing import Optional, Tuple
from urllib.parse import urljoin

# Mapping of English word ratings to numeric integers
RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}

def clean_price(price_text: str) -> float:
    """Extract a positive floating point value from price strings like '£51.77'."""
    if not price_text:
        raise ValueError("Price text cannot be empty")
    
    # Extract digits and decimal point
    match = re.search(r"(\d+(?:\.\d+)?)", price_text)
    if not match:
        raise ValueError(f"Could not parse numeric price from '{price_text}'")
    
    val = float(match.group(1))
    if val <= 0:
        raise ValueError(f"Price must be strictly positive, got {val}")
    return val

def clean_rating(rating_text: str) -> int:
    """Map star rating text ('One', 'Two', 'Three', 'Four', 'Five') to integer 1-5."""
    if not rating_text:
        raise ValueError("Rating text cannot be empty")
    
    key = rating_text.strip().lower()
    if key not in RATING_MAP:
        raise ValueError(f"Unknown star rating: '{rating_text}'")
    return RATING_MAP[key]

def clean_availability(availability_text: str) -> Tuple[bool, int]:
    """Parse availability string like 'In stock (22 available)' into (in_stock, count)."""
    if not availability_text:
        return False, 0
    
    text = availability_text.strip()
    is_in_stock = "in stock" in text.lower()
    
    # Extract count if present e.g. (22 available)
    match = re.search(r"\((\d+)\s+available\)", text, re.IGNORECASE)
    count = int(match.group(1)) if match else (1 if is_in_stock else 0)
    
    return is_in_stock, count

def to_absolute_url(base_url: str, relative_url: str) -> str:
    """Safely resolve relative href into an absolute URL."""
    if not relative_url:
        raise ValueError("Relative URL cannot be empty")
    return urljoin(base_url, relative_url.strip())

def clean_description(desc: Optional[str]) -> Optional[str]:
    """Clean book description whitespace; return None if empty."""
    if not desc:
        return None
    cleaned = desc.strip()
    return cleaned if cleaned else None
