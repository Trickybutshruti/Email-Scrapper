# src/exporter.py

import pandas as pd
import os

RESULTS_FILE = "data/results.xlsx"

def save_to_excel(data: dict):
    """Append result to results.xlsx file."""
    df_new = pd.DataFrame([data])
    if os.path.exists(RESULTS_FILE):
        df_existing = pd.read_excel(RESULTS_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_excel(RESULTS_FILE, index=False)
