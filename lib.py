import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Initialize the browser
options = Options()
options.headless = False  # Set to True to run in the background
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Log in
    driver.get("https://www.linkedin.com/login")
    
    # Updated email/password fields
    email_field = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
    email_field.send_keys("your@email.id")

    password_field = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
    password_field.send_keys("yourpassword")

    # Updated sign-in button selector
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]")))
    sign_in_button.click()

    # Step 2: Navigate to Alumni Page
    driver.get("https://www.linkedin.com/alumni")
    
    # Wait for the alumni page container (generic)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alumni-page')]")))

    # Step 3: Apply Filters
    universities = ["List", "of", "companies", "or", "universities"]

    for uni in universities:
        try:
            # Updated "Show more filters" button
            show_more_filters = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Expand filters')]")))
            show_more_filters.click()

            # Updated "Add school" button
            add_school_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add school')]")))
            add_school_btn.click()

            # Enter school/company name
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'school or university')]")))
            search_input.send_keys(uni)
            time.sleep(random.uniform(1, 2))
            search_input.send_keys(Keys.ARROW_DOWN + Keys.RETURN)
            time.sleep(2)

            # Scroll to load profiles
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Find "Connect" buttons
            connect_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Connect')]")

            for button in connect_buttons:
                try:
                    button.click()
                    # Handle "Add note" modal
                    add_note_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add note')]")))
                    add_note_btn.click()

                    note_field = wait.until(EC.presence_of_element_located((By.ID, "custom-message")))
                    note_field.send_keys("Hi! I’d like to connect and learn from your experience.")
                    
                    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Send now')]")))
                    send_btn.click()
                    time.sleep(random.uniform(2, 4))  # Avoid rate limits
                except Exception as e:
                    print(f"Failed to send request: {e}")
                    continue

            # Reset filters
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Clear all filters')]")))
            reset_btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error processing {uni}: {e}")
            continue

except Exception as e:
    print(f"Script failed: {e}")

finally:
    driver.quit()