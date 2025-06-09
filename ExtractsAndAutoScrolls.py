#This code extracts, autoscrolls in browser and captures all data till the end. Added wait time of 3 seconds in between each parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def extract_post_yes_no_with_scroll():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 1: Open site
        driver.get("https://search.dca.ca.gov/?BD=19&TP=DC")

        # Step 2: Fill in form
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys("Smith")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "licenseType"))).send_keys("Certified Public Accountant")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "srchSubmitHome"))).click()

        # Step 3: Wait for first result
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.post.yes, article.post.no')))
        print("⏳ Starting full extraction (yes + no)...\n")

        parsed_count = 0

        for i in range(300):
            try:
                # Try both 'post yes' and 'post no'
                article = driver.find_element(By.CSS_SELECTOR, f'article.post.yes[id="{i}"], article.post.no[id="{i}"]')

                # Try to find and parse .actions
                try:
                    actions_ul = article.find_element(By.CSS_SELECTOR, "ul.actions")
                    li_items = actions_ul.find_elements(By.TAG_NAME, "li")

                    if not li_items:
                        print(f"🚫 Skipping ID {i}: .actions has no <li>")
                        continue

                    print(f"--- Result ID: {i} ---")
                    for li in li_items:
                        text = li.text.strip()
                        if text:
                            print(text)
                    print("----------------------\n")

                    parsed_count += 1

                    # Scroll every 15 successful parses
                    if parsed_count % 15 == 0:
                        print("🔄 Scrolling and waiting 3 seconds...")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)

                except NoSuchElementException:
                    print(f"🚫 Skipping ID {i}: .actions block missing")

            except NoSuchElementException:
                print(f"❌ ID {i} not found as 'post yes' or 'post no'")

    except TimeoutException:
        print("❌ Timeout during initial load.")

    finally:
        input("✅ Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    extract_post_yes_no_with_scroll()
