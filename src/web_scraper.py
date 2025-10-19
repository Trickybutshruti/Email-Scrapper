# src/web_scraper.py

"""
Automatic web search simulation to identify company details.
Uses DuckDuckGo search (open-source and free) to fetch top snippets.
"""

from duckduckgo_search import DDGS
import re

def get_company_sector(company: str) -> str:
    """
    Uses DuckDuckGo to search the web for company info and extract likely sector.
    """
    if not company:
        return "Unknown"

    query = f"{company} company industry sector"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
    except Exception:
        return "Web search failed"

    text_blob = " ".join(r.get("body", "") for r in results).lower()

    # Basic keyword-based pattern detection
    sector_keywords = {
        "information technology": ["it services", "software", "consulting", "technology"],
        "banking": ["bank", "finance", "financial services"],
        "automobile": ["automobile", "automotive", "vehicles", "cars"],
        "e-commerce": ["ecommerce", "online shopping", "retail"],
        "energy": ["energy", "oil", "gas", "petrochemical"],
        "telecom": ["telecom", "communication", "wireless", "internet"],
        "education": ["university", "school", "education", "edtech"],
        "healthcare": ["hospital", "pharma", "biotech", "healthcare"],
        "manufacturing": ["factory", "manufacturing", "production"],
    }

    for sector, keywords in sector_keywords.items():
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", text_blob):
                return sector.capitalize()

    return "Unidentified"
