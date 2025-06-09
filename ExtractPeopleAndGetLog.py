#This code parses data from html and css level and extracts from the browser automation and shows in terminal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def extract_all_articles():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 1. Go to site
        driver.get("https://search.dca.ca.gov/?BD=19&TP=DC")

        # 2. Fill last name
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lastName"))
        ).send_keys("Smith")

        # 3. Fill license type
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "licenseType"))
        ).send_keys("Certified Public Accountant")

        # 4. Click search
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "srchSubmitHome"))
        ).click()

        print("⏳ Waiting for all result articles...")

        # 5. Wait for results
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article.post.yes'))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, 'article.post.yes')

        print(f"\n🔍 Found {len(articles)} results. Extracting each:\n")

        for i, article in enumerate(articles):
            try:
                actions_ul = article.find_element(By.CSS_SELECTOR, "ul.actions")
                li_items = actions_ul.find_elements(By.TAG_NAME, "li")
                print(f"--- Result #{i + 1} ---")
                for li in li_items:
                    text = li.text.strip()
                    if text:
                        print(text)
                print("----------------------\n")
            except Exception as e:
                print(f"⚠️ Skipping article {i} due to error: {e}")

    except TimeoutException:
        print("❌ Timeout: No result block found.")

    finally:
        input("✅ Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    extract_all_articles()
