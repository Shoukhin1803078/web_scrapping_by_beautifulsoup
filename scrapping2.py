# Both Selenium and BeautifulSoup are used for web scraping.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# ---------------------
# LOGIN
# ---------------------

driver.get("https://app.airwork.ai/login")
time.sleep(3)

driver.find_element(By.NAME, "email").send_keys(EMAIL)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(5)
print("Login Successful")

# ---------------------
# COLLECT JOB LINKS (BS4)
# ---------------------

soup = BeautifulSoup(driver.page_source, "html.parser")

job_links = []

for a in soup.select("main a"):
    link = a.get("href")
    if link:
        job_links.append(link)

print("Total jobs found:", len(job_links))

# ---------------------
# VISIT EACH JOB
# ---------------------

for link in job_links:

    full_link = "https://app.airwork.ai" + link if link.startswith("/") else link
    print("Opening:", full_link)

    driver.get(full_link)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # ---------------- DATA EXTRACTION ----------------

    def safe_text(selector, by="css"):
        try:
            if by == "css":
                tag = soup.select_one(selector)
            else:
                tag = soup.find(id=selector)
            return tag.get_text(strip=True) if tag else ""
        except:
            return ""

    # By ID
    summary = safe_text("job-summary", by="id")
    description = safe_text("job-description", by="id")

    # CSS
    catchphrase = safe_text("div.flex.flex-1.flex-col.gap-0\\.5 p")
    title = safe_text("div.flex.flex-1.flex-col.gap-0\\.5 h1")

    # XPATH alternative → BS4 doesn't support XPath
    # so we simulate via text matching

    def find_by_label(label):
        try:
            span = soup.find("span", string=label)
            return span.find_next("span").get_text(strip=True)
        except:
            return ""

    salary = find_by_label("Salary range")
    job_type = find_by_label("Type")
    job_nature = find_by_label("Nature")

    # ---------------- PRINT ----------------

    print("Catchphrase:", catchphrase)
    print("Title:", title)
    print("Salary:", salary)
    print("Type:", job_type)
    print("Nature:", job_nature)
    print("Summary:", summary)
    print("Description:", description)
    print("----------------------")

driver.quit()