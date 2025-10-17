# app/main_app.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.email_parser import extract_domain, extract_company_name
from src.company_identifier import identify_sector
from src.exporter import save_to_excel
from src.utils import current_timestamp

RESULTS_FILE = "data/results.xlsx"

# Streamlit page setup
st.set_page_config(page_title="Email → Company Identifier", page_icon="📧")

st.title("📧 Email → Company & Sector Identifier Tool")
st.write("Enter an email address to find the related company and sector.")

email = st.text_input("Enter email address:", placeholder="e.g., abhinav@infosys.com")

if st.button("Identify"):
    if not email:
        st.warning("⚠️ Please enter an email address first.")
    else:
        domain = extract_domain(email)
        company = extract_company_name(domain)
        sector = identify_sector(company)

        if not domain:
            st.error("❌ Invalid email address!")
        else:
            st.success(f"✅ Company: **{company}**")
            st.info(f"🌐 Domain: {domain}")
            st.write(f"🏭 Sector: {sector}")

            result = {
                "Timestamp": current_timestamp(),
                "Email": email,
                "Domain": domain,
                "Company": company,
                "Sector": sector
            }
            save_to_excel(result)
            st.success("Result saved to Excel ✅")

# Show existing data
if os.path.exists(RESULTS_FILE):
    st.subheader("📊 Previous Results")
    df = pd.read_excel(RESULTS_FILE)
    st.dataframe(df)
