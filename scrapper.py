#Adds status column in excel output for exact matches

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    return text.replace("\xa0", " ").strip()

def process_single_name(first_name, last_name):
    options = Options()
    options.add_argument("--window-size=1000,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    FIELDS = [
        "First Name", "Middle Name", "Last Name", "License Number", "License Type",
        "License Status", "Expiration Date", "Secondary Status", "City", "State", "County", "Zip", "Match Status"
    ]

    results = []
    match_found = False

    try:
        driver.get("https://search.dca.ca.gov/?BD=19&TP=DC")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(first_name)
        driver.find_element(By.ID, "lastName").send_keys(last_name)
        driver.find_element(By.ID, "licenseType").send_keys("Certified Public Accountant")
        driver.find_element(By.ID, "srchSubmitHome").click()

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.post')))
        except TimeoutException:
            print(f"❌ No results returned for: {first_name} {last_name}")
            return [{
                "First Name": first_name,
                "Middle Name": "Not Found",
                "Last Name": last_name,
                "License Number": "Not Found",
                "License Type": "Not Found",
                "License Status": "Not Found",
                "Expiration Date": "Not Found",
                "Secondary Status": "Not Found",
                "City": "Not Found",
                "State": "Not Found",
                "County": "Not Found",
                "Zip": "Not Found",
                "Match Status": "Not Found"
            }]

        last_count, retries = 0, 0
        while retries < 10:
            articles = driver.find_elements(By.CSS_SELECTOR, 'article.post')
            current_count = len(articles)
            if current_count > last_count:
                last_count = current_count
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                retries = 0
            else:
                retries += 1

        print(f"\n🔍 Found {last_count} total records for: {first_name} {last_name}")

        for idx, article in enumerate(driver.find_elements(By.CSS_SELECTOR, 'article.post')):
            data = {field: "" for field in FIELDS}
            try:
                li_items = article.find_elements(By.CSS_SELECTOR, "ul.actions li")
                for li in li_items:
                    html = li.get_attribute("innerHTML")
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    if "<h3>" in html:
                        try:
                            last, first_middle = text.split(",", 1)
                            name_parts = first_middle.strip().split()
                            data["Last Name"] = clean_text(last)
                            data["First Name"] = name_parts[0] if name_parts else ""
                            data["Middle Name"] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                        except ValueError:
                            data["Last Name"] = text
                    elif ":" in text:
                        key, value = [clean_text(x) for x in text.split(":", 1)]
                        if key in data:
                            data[key] = value

                print(f"📄 Record #{idx}")
                for k, v in data.items():
                    print(f"   {k}: {v}")
                print("")

                if (data["State"].strip().lower() == "california" and
                    data["First Name"].strip().lower() == first_name.strip().lower() and
                    data["Last Name"].strip().lower() == last_name.strip().lower()):
                    data["Match Status"] = "Matched"
                    results.append(data)
                    match_found = True
                    print(f"✅ Match found for: {first_name} {last_name}")
            except Exception as e:
                print(f"⚠️ Error parsing record #{idx}: {e}")

    finally:
        driver.quit()

        if not match_found:
            print(f"❌ No exact match found in California for: {first_name} {last_name}")
            results.append({
                "First Name": first_name,
                "Middle Name": "Not Found",
                "Last Name": last_name,
                "License Number": "Not Found",
                "License Type": "Not Found",
                "License Status": "Not Found",
                "Expiration Date": "Not Found",
                "Secondary Status": "Not Found",
                "City": "Not Found",
                "State": "Not Found",
                "County": "Not Found",
                "Zip": "Not Found",
                "Match Status": "Not Found"
            })

        return results

def main():
    df = pd.read_excel("names.xlsx", skiprows=3)
    all_results = []
    for _, row in df.iterrows():
        first_name = str(row[0]).strip()
        last_name = str(row[1]).strip()
        if first_name and last_name:
            all_results.extend(process_single_name(first_name, last_name))

    pd.DataFrame(all_results).to_excel("california_matches.xlsx", index=False)
    print("\n✅ Done! Results saved to california_matches.xlsx")

if __name__ == "__main__":
    main()
