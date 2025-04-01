import re
import requests
from googlesearch import search

def find_linkedin_profiles(name, organization):
    query = f'site:linkedin.com/in "{name}" "{organization}"'
    print("Searching for LinkedIn profile using query:", query)
    profiles = []
    try:
        for url in search(query, num_results=10):
            if "linkedin.com/in" in url:
                profiles.append(url)
    except Exception as e:
        print("Error during LinkedIn search:", e)
    return profiles

def is_valid_email(email):
    # Filters to exclude unwanted or junk emails
    blacklist_keywords = ['sentry.io', '.png', '.jpg', '.jpeg', '.svg', 'example.com']
    whitelist_domains = ['nyu.edu']

    if any(bad in email.lower() for bad in blacklist_keywords):
        return False
    if any(email.lower().endswith(domain) for domain in whitelist_domains):
        return True
    return False

def find_emails(name, organization):
    query = f'"{name}" "{organization}" email'
    print("Searching for emails using query:", query)
    emails = set()
    try:
        for url in search(query, num_results=10):
            if not url or not url.startswith("http"):
                continue  # skip invalid URLs
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    found_emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", response.text)
                    for email in found_emails:
                        if is_valid_email(email):
                            emails.add(email)
            except Exception as inner_e:
                print(f"Failed to process {url}: {inner_e}")
    except Exception as e:
        print("Error during email search:", e)
    return list(emails)

def main():
    print("=== Email and LinkedIn Profile Finder ===")
    name = input("Enter the person's name: ").strip()
    organization = input("Enter the organization: ").strip()

    linkedin_profiles = find_linkedin_profiles(name, organization)
    if linkedin_profiles:
        print("\nPossible LinkedIn Profiles:")
        for i, profile in enumerate(linkedin_profiles, 1):
            print(f"{i}. {profile}")
    else:
        print("\nNo LinkedIn profiles found.")

    emails = find_emails(name, organization)
    if emails:
        print("\nFound Emails:")
        for email in emails:
            print(email)
    else:
        print("\nNo valid emails found.")

if __name__ == "__main__":
    main()
