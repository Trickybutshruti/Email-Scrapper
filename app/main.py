# app/main_app.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import time

from src.email_parser import extract_domain, extract_company_name
from src.company_identifier import identify_sector
from src.exporter import save_to_excel
from src.utils import current_timestamp

RESULTS_FILE = "data/results.xlsx"

# --- Streamlit Page Setup ---
st.set_page_config(page_title="📧 Email → Company Identifier", page_icon="💼", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        text-align: center;
        color: #2C3E50;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #5D6D7E;
    }
    .result-box {
        background-color: #F8F9F9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 class='main-title'>📧 Email → Company & Sector Identifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter an email or upload a list to instantly identify the company, sector, and more.</p>", unsafe_allow_html=True)

# --- Tabs for Single/Bulk Mode ---
tab1, tab2 = st.tabs(["🔹 Single Email", "📂 Bulk Upload"])

# --- Tab 1: Single Email Mode ---
with tab1:
    email = st.text_input("Enter Email Address:", placeholder="e.g., abhinav@infosys.com")

    if st.button("Identify Company"):
        if not email:
            st.warning("⚠️ Please enter an email address.")
        else:
            with st.spinner("🔍 Analyzing email... Please wait."):
                time.sleep(1.2)  # simulate loading
                domain = extract_domain(email)
                company = extract_company_name(domain)
                company_info = identify_sector(domain or company)  # Returns dict with sector, year, etc.

            if not domain:
                st.error("❌ Invalid or generic email address!")
            else:
                st.success("✅ Company Identified!")
                with st.container():
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.markdown(f"**🏢 Company:** {company_info.get('company', company)}")
                    st.markdown(f"**🌐 Domain:** {domain}")
                    st.markdown(f"**🏭 Sector:** {company_info.get('sector', 'Unknown')}")
                    st.markdown(f"**📅 Year Founded:** {company_info.get('year_founded', 'N/A')}")
                    if company_info.get('website'):
                        st.markdown(f"**🔗 Website:** [{company_info['website']}]({company_info['website']})")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Save Result
                result = {
                    "Timestamp": current_timestamp(),
                    "Email": email,
                    "Domain": domain,
                    "Company": company,
                    "Sector": company_info.get('sector', 'Unknown'),
                    "Year Founded": company_info.get('year_founded', 'N/A'),
                    "Website": company_info.get('website', '')
                }
                save_to_excel(result)
                st.toast("💾 Result saved to Excel!", icon="✅")

# --- Tab 2: Bulk Upload ---
with tab2:
    uploaded_file = st.file_uploader("Upload CSV file with a column named 'email'", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "email" not in df.columns:
            st.error("❌ CSV must contain a column named 'email'.")
        else:
            st.info(f"Processing {len(df)} emails...")
            results = []
            progress = st.progress(0)
            for i, row in enumerate(df["email"]):
                domain = extract_domain(row)
                company = extract_company_name(domain)
                company_info = identify_sector(domain or company)
                result = {
                    "Timestamp": current_timestamp(),
                    "Email": row,
                    "Domain": domain,
                    "Company": company,
                    "Sector": company_info.get('sector', 'Unknown'),
                    "Year Founded": company_info.get('year_founded', 'N/A'),
                    "Website": company_info.get('website', '')
                }
                results.append(result)
                progress.progress((i + 1) / len(df))
                time.sleep(0.1)
            st.success("✅ Bulk processing complete!")
            results_df = pd.DataFrame(results)
            st.dataframe(results_df)
            results_df.to_excel(RESULTS_FILE, index=False)
            st.download_button("⬇️ Download Results", data=results_df.to_csv(index=False), file_name="email_results.csv")

# --- Display Previous Results ---
if os.path.exists(RESULTS_FILE):
    st.divider()
    st.subheader("📊 Previous Results")
    df = pd.read_excel(RESULTS_FILE)
    df = df.astype(str)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")

    # Add a clear button
    if st.button("🗑️ Clear All Previous Results"):
        os.remove(RESULTS_FILE)
        st.warning("All previous records have been deleted ❌")
        st.rerun()
else:
    st.info("No previous results found.")