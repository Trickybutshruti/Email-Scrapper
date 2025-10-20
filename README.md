# 📧 Email-Scrapper

A web-based tool that extracts **company name, industry sector, year founded, and website** from an email address. The tool supports **single email input** and **bulk CSV uploads**, and saves results in an Excel file for future reference.

---

## 🔹 Features

* Identify **company, sector, year founded, and domain** from email addresses
* **Single email input** or **bulk CSV upload**
* **Fast lookup** using a cleaned dataset
* **Fallback web scraping** for rare or unseen domains
* Export results to Excel (`data/results.xlsx`)
* Option to **clear previous history**

---

## 🖥 Requirements

* Python 3.12 or higher
* `pip` for package installation
* Streamlit, Pandas, Playwright, tldextract, openpyxl

---

## ⚡ Step-by-Step Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Email-Scrapper.git
cd Email-Scrapper
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

* **Windows:**

```bash
venv\Scripts\activate
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

### 4️⃣ Run the Web App

```bash
streamlit run app/main_app.py
```

* The app will open in your default browser automatically.
* Enter an email or upload a CSV file to see results.
* All outputs are saved in `data/results.xlsx`.

---

## 📝 Key Points

* The dataset used is **cleaned** to retain only essential information (domain, sector, year founded, website).
* Web scraping is used **only if a domain is not found in the dataset**.
* Automated Google searches may occasionally be blocked, so fallback scraping is primarily for **rare or unseen domains**.

---

### Future Enhancements

* More detailed **analytics for bulk uploads**
* Improved **web scraping for dynamic websites**

---
