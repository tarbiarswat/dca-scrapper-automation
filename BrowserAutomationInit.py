#This code opens the browser, automatically gives predefined input and clicks on search button

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def input_names_and_search():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open DCA License Search site
    driver.get("https://search.dca.ca.gov/?BD=19&TP=DC")

    # Input First Name
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "firstName"))
    ).send_keys("John")

    # Input Last Name
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lastName"))
    ).send_keys("Smith")

    # Click the Advanced Search submit button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "srchSubmitHome"))
    ).click()

    print("✅ Entered First Name, Last Name and clicked Search.")
    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    input_names_and_search()
