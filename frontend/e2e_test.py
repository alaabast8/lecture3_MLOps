import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # Import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def run_e2e_test():
    # --- FIX: Configure Chrome for Headless CI Environment ---
    options = Options()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--no-sandbox") # Required for Linux/CI
    options.add_argument("--disable-dev-shm-usage") # Overcome resource limits
    
    driver = webdriver.Chrome(options=options)

    # Fallback to localhost if env var is missing
    base_url = os.getenv("FRONTEND_URL")

    try:
        print(f"Starting E2E Test on {base_url}...")
        driver.get(base_url) 

        wait = WebDriverWait(driver, 10)
        
        header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "My Fullstack App" in header.text
        print("[PASS] Title verified.")

        item_name = "Selenium Test Item"
        item_desc = "Created via Python Selenium"

        name_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='item-name-input']")
        desc_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='item-description-input']")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-button']")

        name_input.send_keys(item_name)
        desc_input.send_keys(item_desc)
        
        submit_btn.click()
        print("Form submitted.")

        xpath_query = f"//li[contains(., '{item_name}')]"
        new_item = wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))
        
        assert item_name in new_item.text
        assert item_desc in new_item.text
        print("[PASS] New item found in the list.")

    except Exception as e:
        print(f"[FAIL] Test Failed: {e}")
        # IMPORTANT: Fail the action if test fails
        exit(1) 
    finally:
        driver.quit()

if __name__ == "__main__":
    run_e2e_test()