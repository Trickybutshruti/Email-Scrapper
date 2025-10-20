from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_company_info(domain: str) -> dict:

    search_query = f"{domain} company industry"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"https://www.google.com/search?q={search_query}")

    time.sleep(2)  

    result_dict = {"company": domain.title(), "sector": "Other / Unidentified", "year_founded": "N/A", "website": ""}

    try:
        # Example: grab first result title
        title_element = driver.find_element(By.CSS_SELECTOR, "h3")
        snippet_element = driver.find_element(By.CSS_SELECTOR, ".VwiC3b")
        result_dict["company"] = title_element.text
        result_dict["sector"] = snippet_element.text[:50]  # show first 50 chars as demo
    except Exception:
        pass
    finally:
        driver.quit()

    return result_dict
