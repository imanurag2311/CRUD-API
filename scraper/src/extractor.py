"""HTML extraction routines using BeautifulSoup.

Extracts data from the specific product area of Books to Scrape:
- Scoped to '#content_inner article.product_page' to avoid false selector matches
- Handles optional book descriptions without crashing
- Captures provenance metadata (source_page and fetched_at)
"""
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from urllib.parse import urljoin
from scraper.src.schemas import RawBookRecord
from scraper.src.normalizer import to_absolute_url

def extract_catalogue_links(html: str, page_url: str) -> Tuple[List[str], Optional[str]]:
    """Extract all book detail links (absolute URLs) and the next page link from a catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Extract book links from product pods
    book_links = []
    pods = soup.select("article.product_pod")
    for pod in pods:
        a_tag = pod.select_one("h3 a")
        if a_tag and a_tag.get("href"):
            raw_href = a_tag["href"]
            abs_url = to_absolute_url(page_url, raw_href)
            book_links.append(abs_url)
            
    # 2. Extract next page link if present
    next_tag = soup.select_one("ul.pager li.next a")
    next_url = None
    if next_tag and next_tag.get("href"):
        next_url = to_absolute_url(page_url, next_tag["href"])
        
    return book_links, next_url

def extract_book_details(html: str, product_url: str, source_page: str, fetched_at: str) -> RawBookRecord:
    """Extract raw product details from a book detail page."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Check if page is valid product page
    article = soup.select_one("article.product_page")
    if not article:
        raise ValueError(f"Could not locate 'article.product_page' on {product_url}")
        
    # Title
    title_tag = article.select_one(".product_main h1")
    title = title_tag.get_text(strip=True) if title_tag else ""
    if not title:
        raise ValueError(f"Missing book title on {product_url}")
        
    # Price text
    price_tag = article.select_one(".product_main p.price_color")
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    
    # Availability text
    avail_tag = article.select_one(".product_main p.instock.availability")
    availability_text = avail_tag.get_text(strip=True) if avail_tag else ""
    
    # Star rating text from class attribute (e.g. ['star-rating', 'Three'])
    rating_tag = article.select_one("p.star-rating")
    rating_text = ""
    if rating_tag and rating_tag.get("class"):
        classes = rating_tag["class"]
        for cls in classes:
            if cls.lower() != "star-rating":
                rating_text = cls
                break
                
    # Description (optional: #product_description ~ p)
    desc_tag = article.select_one("#product_description ~ p")
    description = desc_tag.get_text(strip=True) if desc_tag else None
    
    return RawBookRecord(
        title=title,
        product_url=product_url,
        price_text=price_text,
        availability_text=availability_text,
        rating_text=rating_text,
        description=description,
        source_page=source_page,
        fetched_at=fetched_at
    )
