from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse 
import tempfile


def setup_driver():
    """
    Sets up Chrome in Incognito mode to avoid LinkedIn's session tracking.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login_to_linkedin(driver, wait, email, password):
    """
    Logs in to LinkedIn and waits if a verification step appears.
    """
    driver.get("https://www.linkedin.com/login")
    
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(5)

    if "checkpoint" in driver.current_url:
        print("🔒 Verification required! Please complete it manually.")
        while "checkpoint" in driver.current_url:
            time.sleep(5)
        print("✅ Verification completed. Continuing...")

def construct_search_url(name, organization, position):
    """
    Constructs a LinkedIn search URL based on name, organization, and position.
    """
    keywords = []
    if name.strip():
        keywords.append(name.strip())
    if organization.strip():
        keywords.append(organization.strip())
    if position.strip():
        keywords.append(position.strip())

    if not keywords:
        print("⚠️ No valid search terms provided! Provide at least organization or position.")
        return None

    query_string = urllib.parse.quote(" ".join(keywords))
    search_url = f"https://www.linkedin.com/search/results/all/?keywords={query_string}&origin=GLOBAL_SEARCH_HEADER"
    return search_url

def select_people_tab(driver, wait):
    """
    Clicks on the 'People' tab in LinkedIn search results.
    """
    try:
        people_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'search-reusables__primary-filter')]/button"))
        )

        is_selected = people_tab.get_attribute("aria-pressed") == "true"
        
        if not is_selected:
            people_tab.click()
            print("✅ Clicked on the 'People' tab.")
            time.sleep(3)
        else:
            print("✅ 'People' tab is already selected.")

    except Exception as e:
        print("❌ Error clicking 'People' tab:", e)

def open_first_profile(driver, wait):
    """
    Opens the first profile in search results by clicking the 'cursor-pointer' div.
    """
    try:
        # Wait for the first profile result div
        first_profile_div = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.linked-area.flex-1.cursor-pointer"))
        )

        print("✅ Clicking the first profile result...")

        # Scroll into view and click using JavaScript to avoid overlay issues
        driver.execute_script("arguments[0].scrollIntoView();", first_profile_div)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", first_profile_div)

        time.sleep(5)
        print(f"✅ Opened first profile: {driver.current_url}")
        return driver.current_url

    except Exception as e:
        print("❌ Error locating or opening the first profile:", e)
        return None

def click_message_button(driver, wait):
    """
    Scrolls down, tries multiple XPath strategies to find and click the 'Message' button.
    Uses JavaScript click as a fallback if needed.
    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    message_xpaths = [
        "//button[contains(@aria-label, 'Message')]",
        "//button[span[text()='Message']]",
        "//button[contains(., 'Message')]",
        "//button[contains(@aria-label, 'InMail')]",
        "//a[contains(@aria-label, 'Message')]"
    ]

    for xpath in message_xpaths:
        try:
            message_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView();", message_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", message_button)
            print(f"✅ Clicked the 'Message' button using XPath: {xpath}")
            return True
        except:
            pass

    print("❌ Could not find the 'Message' button using any known XPath.")
    return False

def send_message_on_profile(driver, wait, message_text):
    """
    1. Clicks the "Message" button on a LinkedIn profile page.
    2. Sends the specified message.
    """
    try:
        if not click_message_button(driver, wait):
            print("⚠️ Message button not found. Exiting.")
            return

        message_box = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Write a message…']"))
        )
        message_box.send_keys(message_text)

        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and contains(@class, 'msg-form__send-button')]")
            )
        )
        send_button.click()
        print("✅ Message sent successfully!")

    except Exception as e:
        print("❌ Error while sending the message:", e)

def main():
    # Example usage of the functions
    linkedin_email = "your_linkedin_email"
    linkedin_password = "your_linkedin_password"
    recipient_name = "John Doe"
    organization = "Example Corp"
    position = "Software Engineer"
    message_text = "Hello! I would like to connect with you."

    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login_to_linkedin(driver, wait, linkedin_email, linkedin_password)
        search_url = construct_search_url(recipient_name, organization, position)
        if search_url:
            driver.get(search_url)
            select_people_tab(driver, wait)
            profile_url = open_first_profile(driver, wait)
            if profile_url:
                send_message_on_profile(driver, wait, message_text)
            else:
                print("❌ LinkedIn profile not found.")
        else:
            print("❌ Invalid search URL.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
