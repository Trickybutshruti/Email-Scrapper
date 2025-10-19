# src/company_identifier.py

import pandas as pd
import os

DATA_PATH = "data/companies_clean.csv"

_cached_df = None

def load_company_data():
    """Load and cache cleaned company data."""
    global _cached_df
    if _cached_df is None and os.path.exists(DATA_PATH):
        _cached_df = pd.read_csv(DATA_PATH)
    return _cached_df


def identify_company_info(company_or_domain: str) -> dict:
    """
    Identify company info (industry, year founded) using the cleaned dataset.
    Returns a dict like: {"industry": "IT", "year_founded": "1981"}
    """
    df = load_company_data()
    if df is None:
        return {"industry": "Unknown", "year_founded": "Unknown"}

    text = str(company_or_domain).lower().strip()

    # Auto-detect column names
    name_col = next((c for c in df.columns if "name" in c.lower()), None)
    domain_col = next((c for c in df.columns if "domain" in c.lower()), None)
    industry_col = next((c for c in df.columns if "industry" in c.lower() or "sector" in c.lower()), None)
    year_col = next((c for c in df.columns if "year" in c.lower()), None)

    if not all([name_col, domain_col, industry_col, year_col]):
        return {"industry": "Invalid dataset structure", "year_founded": "Unknown"}

    # Try domain match first
    match = df[df[domain_col].str.contains(text, na=False)]
    if not match.empty:
        row = match.iloc[0]
        return {
            "industry": str(row[industry_col]).title(),
            "year_founded": str(row[year_col]).capitalize(),
        }

    # Try company name match
    match = df[df[name_col].str.contains(text, na=False)]
    if not match.empty:
        row = match.iloc[0]
        return {
            "industry": str(row[industry_col]).title(),
            "year_founded": str(row[year_col]).capitalize(),
        }

    return {"industry": "Other / Unidentified", "year_founded": "Unknown"}
