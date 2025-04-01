# LinkedIn + Email Automation App

Find the app here https://inconnect.streamlit.app/

This application allows users to automate outreach tasks by:

- Scraping LinkedIn profiles based on name, organization, and position
- Finding professional email addresses using the Hunter.io API
- Sending LinkedIn messages using Selenium
- Sending emails through Gmail using Selenium browser automation

All through a simple and interactive Streamlit interface.

---

## Features

- 📄 Input fields for credentials and target information
- 🔗 Automate LinkedIn profile search and messaging
- 📧 Find email addresses using Hunter.io and send Gmail messages
- 🧩 Modular backend with Selenium automation scripts

---

## Project Structure
    
    
    LinkedIn_Email_Automation/
    ├── app.py                  # Main Streamlit application file       
    ├── requirements.txt        # Python dependencies
    ├── scripts/                  # Backend automation scripts
    │   ├── email_id_finder.py           # Find email addresses using Hunter.io API
    │   ├── LinkedInAutomation.py         # LinkedIn profile scraping and messaging
    │   └── EmailAutomation.py         #   Gmail automation for sending emails
    └── README.md              # This file
    

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/RSaivarsha/LinkedIn_Email_Automation.git
cd LinkedIn_Email_Automation

```
### 2. Install dependencies

```bash
pip install -r requirements.txt
```
### 3. Set up environment variables
Create a `.env` file in the root directory and add your credentials:

```
.env file
HUNTER_API_KEY=your_hunter_api_key
GMAIL_EMAIL=your_gmail_email
GMAIL_PASSWORD=your_gmail_password
```
### 4. Run the application

```bash
streamlit run app.py
```

