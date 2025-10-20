# src/company_identifier.py

import pandas as pd
import os

DATA_PATH = "data/companies_clean.csv"

# Load and cache data
def load_company_data():
    """Load cleaned company dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Cleaned data file not found at {DATA_PATH}. Run data_cleaner.py first.")
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

company_data = load_company_data()


def identify_sector(query: str) -> dict:
    """
    Identify company sector, year founded, and website from dataset.
    Returns a dictionary with {company, sector, year_founded, website}.
    """

    if not query:
        return {"company": "Unknown", "sector": "Unknown", "year_founded": "N/A", "website": ""}

    query = str(query).lower()

    # Try to match by domain first
    match = company_data[company_data["domain"].str.contains(query, na=False)]
    if match.empty:
        # Try matching by company name
        match = company_data[company_data["name"].str.contains(query, na=False)]

    if not match.empty:
        row = match.iloc[0]
        return {
            "company": row.get("name", "Unknown").title(),
            "sector": row.get("industry", "Unknown").title(),
            "year_founded": row.get("year founded", "N/A"),
            "website": f"https://{row['domain']}" if "domain" in row and pd.notna(row["domain"]) else ""
        }

    # Default fallback
    return {
        "company": query.title(),
        "sector": "Other / Unidentified",
        "year_founded": "N/A",
        "website": ""
    }
