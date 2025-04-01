import streamlit as st
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
from scripts.EmailAutomation import send_email
from scripts.LinkedInAutomation import setup_driver, login_to_linkedin, construct_search_url, select_people_tab, open_first_profile, send_message_on_profile
from scripts.email_id_finder import get_domain_from_organization, find_email

load_dotenv()

st.title("🚀 LinkedIn & Email Automation")

# Sidebar credentials
st.sidebar.header("Your Credentials")
linkedin_email = st.sidebar.text_input("LinkedIn Email")
linkedin_password = st.sidebar.text_input("LinkedIn Password", type="password")
gmail_email = st.sidebar.text_input("Gmail Email")
gmail_password = st.sidebar.text_input("Gmail Password", type="password")

# Recipient details
st.header("Recipient Information")
recipient_name = st.text_input("Recipient Full Name")
organization = st.text_input("Organization")
position = st.text_input("Position (Optional)")

# LinkedIn message
linkedin_message = st.text_area("LinkedIn Message")

# Email details
email_subject = st.text_input("Email Subject")
email_message = st.text_area("Email Message")

# LinkedIn automation button
if st.button("🔗 Automate LinkedIn"):
    with st.spinner("Automating LinkedIn Message..."):
        driver = setup_driver()
        wait = WebDriverWait(driver, 20)
        try:
            login_to_linkedin(driver, wait, linkedin_email, linkedin_password)
            search_url = construct_search_url(recipient_name, organization, position)
            driver.get(search_url)
            select_people_tab(driver, wait)
            profile_url = open_first_profile(driver, wait)
            if profile_url:
                send_message_on_profile(driver, wait, linkedin_message)
                st.success("✅ LinkedIn message sent successfully!")
            else:
                st.error("❌ LinkedIn profile not found.")
        except Exception as e:
            st.error(f"LinkedIn automation error: {e}")
        finally:
            driver.quit()

# Email automation button
if st.button("📧 Automate Email"):
    with st.spinner("Finding email..."):
        domain = get_domain_from_organization(organization)
        if domain:
            email = find_email(recipient_name, domain)
            if email:
                st.success(f"Email found: {email}")
                with st.spinner("Sending email via Gmail..."):
                    try:
                        send_email(gmail_email, gmail_password, email, email_subject, email_message)
                        st.success("✅ Email sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending email: {e}")
            else:
                st.error("❌ Email not found.")
        else:
            st.error("❌ Domain not found for the organization.")
