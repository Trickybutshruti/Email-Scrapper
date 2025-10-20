import pandas as pd
import os
from src.web_scraper import scrape_company_info  

DATA_PATH = "data/companies_clean.csv"

def load_company_data():
    """Load cleaned company dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Cleaned data file not found at {DATA_PATH}. Run data_cleaner.py first.")
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

company_data = load_company_data()


def identify_sector(query: str) -> dict:
   
    if not query:
        return {"company": "Unknown", "sector": "Unknown", "year_founded": "N/A", "website": ""}

    query = str(query).lower()
    
    match = company_data[company_data["domain"].str.contains(query, na=False)]
    if match.empty:
        match = company_data[company_data["name"].str.contains(query, na=False)]

    if not match.empty:
        row = match.iloc[0]
        return {
            "company": row.get("name", "Unknown").title(),
            "sector": row.get("industry", "Unknown").title(),
            "year_founded": row.get("year founded", "N/A"),
            "website": f"https://{row['domain']}" if "domain" in row and pd.notna(row["domain"]) else ""
        }

    print(f"⚡ No match in dataset, trying Google search for: {query}")
    scraped_info = scrape_company_info(query)
    return {
        "company": scraped_info.get("company", query.title()),
        "sector": scraped_info.get("sector", "Other / Unidentified"),
        "year_founded": scraped_info.get("year_founded", "N/A"),
        "website": scraped_info.get("website", "")
    }
