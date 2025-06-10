#This code reads name inputs dynamically from excel, scrap and save results in a new excel
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
        "ID", "First Name", "Middle Name", "Last Name", "License Number", "License Type",
        "License Status", "Expiration Date", "Secondary Status", "City", "State", "County", "Zip"
    ]

    results = []
    try:
        driver.get("https://search.dca.ca.gov/?BD=19&TP=DC")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(first_name)
        driver.find_element(By.ID, "lastName").send_keys(last_name)
        driver.find_element(By.ID, "licenseType").send_keys("Certified Public Accountant")
        driver.find_element(By.ID, "srchSubmitHome").click()

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.post')))

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

        print(f"\n🔍 Processing {current_count} results for: {first_name} {last_name}")
        match_found = False
        id_counter = 0

        for article in driver.find_elements(By.CSS_SELECTOR, 'article.post'):
            row = {field: "" for field in FIELDS}
            row["ID"] = id_counter
            try:
                for li in article.find_elements(By.CSS_SELECTOR, "ul.actions li"):
                    html = li.get_attribute("innerHTML")
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    if "<h3>" in html:
                        try:
                            last, first_middle = text.split(",", 1)
                            name_parts = first_middle.strip().split()
                            row["Last Name"] = clean_text(last)
                            row["First Name"] = name_parts[0] if name_parts else ""
                            row["Middle Name"] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                        except:
                            row["Last Name"] = text
                    elif ":" in text:
                        key, value = [clean_text(x) for x in text.split(":", 1)]
                        if key in row:
                            row[key] = value

                print(f"🔹 ID {id_counter} → {row}")

                if (
                    row["First Name"].lower() == first_name.lower() and
                    row["Last Name"].lower() == last_name.lower() and
                    row["State"].lower() == "california"
                ):
                    results.append(row)
                    print(f"✅ MATCH FOUND (CA) for: {first_name} {last_name}")
                    match_found = True

            except Exception as e:
                print(f"⚠️ Error parsing article ID {id_counter}: {e}")
            id_counter += 1

        if not match_found:
            print(f"❌ No exact CA match: {first_name} {last_name}")
            results.append({
                "ID": "N/A",
                "First Name": first_name,
                "Middle Name": "",
                "Last Name": last_name,
                "License Number": "Not Found",
                "License Type": "Not Found",
                "License Status": "Not Found",
                "Expiration Date": "Not Found",
                "Secondary Status": "Not Found",
                "City": "Not Found",
                "State": "Not Found",
                "County": "Not Found",
                "Zip": "Not Found"
            })

    except TimeoutException:
        print(f"⏱️ Timeout for: {first_name} {last_name}")
        results.append({
            "ID": "N/A",
            "First Name": first_name,
            "Middle Name": "",
            "Last Name": last_name,
            "License Number": "Timeout",
            "License Type": "Timeout",
            "License Status": "Timeout",
            "Expiration Date": "Timeout",
            "Secondary Status": "Timeout",
            "City": "Timeout",
            "State": "Timeout",
            "County": "Timeout",
            "Zip": "Timeout"
        })
    finally:
        driver.quit()
        return results

def main():
    df = pd.read_excel("names.xlsx", skiprows=3)
    all_results = []

    for _, row in df.iterrows():
        first_name = str(row[0]).strip()
        last_name = str(row[1]).strip()
        if first_name and last_name:
            results = process_single_name(first_name, last_name)
            all_results.extend(results)

    pd.DataFrame(all_results).to_excel("california_matches.xlsx", index=False)
    print("\n✅ All results saved to california_matches.xlsx")

if __name__ == "__main__":
    main()
