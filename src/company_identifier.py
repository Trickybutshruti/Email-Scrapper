# src/company_identifier.py

"""
Maps company names to known sectors.
Later, this can use web_scraper.py for real-time info.
"""

def identify_sector(company: str) -> str:
    """Simple keyword-based sector mapping."""
    if not company:
        return "Unknown"

    company_lower = company.lower()
    sector_map = {
        "infosys": "Information Technology",
        "tcs": "Information Technology",
        "wipro": "Information Technology",
        "amazon": "E-Commerce",
        "flipkart": "E-Commerce",
        "reliance": "Energy / Telecom",
        "icici": "Banking",
        "hdfc": "Banking",
        "mahindra": "Automobile",
        "maruti": "Automobile",
        "tata": "Conglomerate",
        "airtel": "Telecommunications"
    }

    for keyword, sector in sector_map.items():
        if keyword in company_lower:
            return sector

    return "Other / Unidentified"
