# scripts/emailtry.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_email(gmail_email, gmail_password, receiver_email, subject, message_body):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AXH0vVvkZ9HaeocFKUxRHFNMSWO5uSddneKqu54SoZnVj3HN6tckJNsuCZCd_6_y6FcXlDIW0OITeQ&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1491657561%3A1743007314660933")

        wait.until(EC.visibility_of_element_located((By.ID, "identifierId"))).send_keys(gmail_email)
        wait.until(EC.element_to_be_clickable((By.ID, "identifierNext"))).click()

        wait.until(EC.visibility_of_element_located((By.NAME, "Passwd"))).send_keys(gmail_password)
        wait.until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()

        wait.until(EC.title_contains("Inbox"))
        time.sleep(2)

        compose_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".T-I.T-I-KE.L3")))
        driver.execute_script("arguments[0].click();", compose_button)
        time.sleep(3)

        active_element = driver.switch_to.active_element
        active_element.send_keys(receiver_email)
        time.sleep(1)

        subject_input = wait.until(EC.visibility_of_element_located((By.NAME, "subjectbox")))
        driver.execute_script("arguments[0].scrollIntoView(true);", subject_input)
        driver.execute_script("arguments[0].click();", subject_input)
        subject_input.send_keys(subject)

        body_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[aria-label='Message Body']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", body_box)
        driver.execute_script("arguments[0].click();", body_box)
        body_box.send_keys(message_body)

        body_box.send_keys(Keys.CONTROL, Keys.ENTER)
        print("Email sent successfully!")
        time.sleep(3)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()
