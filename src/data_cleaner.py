# src/data_cleaner.py

import pandas as pd

RAW_PATH = "data/companies_raw.csv"
CLEAN_PATH = "data/companies_clean.csv"

def clean_company_data():
    """Clean the raw company-domain-sector dataset."""
    df = pd.read_csv(RAW_PATH)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    columns_to_keep = ["name" , "domain" , "year founded" , "industry"]
    df = df[[col for col in columns_to_keep if col in df.columns]]

    df = df.dropna().drop_duplicates()

    for col in ["name" , "domain" , "year founded" , "industry"]:
        df[col] = df[col].astype(str).str.strip().str.lower()

    df.to_csv(CLEAN_PATH, index=False)
    print(f"✅ Cleaned data saved to {CLEAN_PATH} ({len(df)} records).")

if __name__ == "__main__":
    clean_company_data()
