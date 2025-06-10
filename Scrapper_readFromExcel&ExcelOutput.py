#This code reads name inputs dynamically from excel, scrap and save results in a new excel
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    return text.replace("\xa0", " ").strip()

def process_single_name(first_name, last_name):
    options = Options()
    #options.add_argument("--start-minimized")
    options.add_argument("--window-size=1000,800")  # Smaller window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.set_window_position(-2000, 0)

    FIELDS = [
        "First Name", "Middle Name", "Last Name", "License Number", "License Type",
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

        # Auto scroll to load all results
        last_count = 0
        retries = 0
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

        print(f"🔍 Total articles found: {last_count}")
        found = False

        for article in driver.find_elements(By.CSS_SELECTOR, 'article.post'):
            try:
                actions_ul = article.find_element(By.CSS_SELECTOR, "ul.actions")
                li_items = actions_ul.find_elements(By.TAG_NAME, "li")
                data = {field: "" for field in FIELDS}

                for li in li_items:
                    text = clean_text(li.text)
                    html = li.get_attribute("innerHTML")
                    if "<h3>" in html:
                        try:
                            last, first_middle = text.split(",", 1)
                            name_parts = first_middle.strip().split()
                            data["Last Name"] = clean_text(last)
                            data["First Name"] = name_parts[0] if len(name_parts) > 0 else ""
                            data["Middle Name"] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                        except ValueError:
                            data["Last Name"] = text
                    elif ":" in text:
                        key, value = [clean_text(x) for x in text.split(":", 1)]
                        if key in data:
                            data[key] = value

                if data["State"].lower() == "california" and \
                   data["First Name"].lower() == first_name.lower() and \
                   data["Last Name"].lower() == last_name.lower():
                    results.append(data)
                    print(f"✅ Exact match found in CA: {first_name} {last_name}")
                    found = True
                else:
                    print(f"🚫 Not exact match or not California: {first_name} {last_name}")

            except Exception as e:
                print(f"⚠️ Error parsing article: {e}")

        if not found:
            print(f"❌ No CA exact match for: {first_name} {last_name}")

    except TimeoutException:
        print(f"⏱️ Timeout for: {first_name} {last_name}")

    finally:
        driver.quit()
        return results

def main():
    df = pd.read_excel("names.xlsx", skiprows=2)  # Starts reading from row 4
    all_results = []

    for index, row in df.iterrows():
        first_name = str(row[0]).strip()
        last_name = str(row[1]).strip()
        if first_name and last_name:
            results = process_single_name(first_name, last_name)
            all_results.extend(results)

    if all_results:
        pd.DataFrame(all_results).to_excel("california_matches.xlsx", index=False)
        print("✅ Exported California matches to 'california_matches.xlsx'")
    else:
        print("❌ No California matches found.")

if __name__ == "__main__":
    main()
