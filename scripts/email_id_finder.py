import requests

# 🔐 Paste your Hunter.io API key here
HUNTER_API_KEY = "Your_Hunter_API_Key"

def get_domain_from_organization(organization):
    """
    Uses Hunter.io's Domain Search API to find the most likely domain from an organization name.
    """
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "company": organization,
        "api_key": HUNTER_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        domain = data.get("data", {}).get("domain")
        if domain:
            print(f"🔍 Found domain for {organization}: {domain}")
            return domain
        else:
            print(f"❌ Could not find domain for {organization}")
    else:
        print(f"⚠️ Error while fetching domain: {response.status_code} - {response.text}")
    return None

def find_email(name, domain):
    """
    Uses Hunter.io Email Finder API to get a professional email by name and domain.
    """
    url = "https://api.hunter.io/v2/email-finder"
    params = {
        "full_name": name,
        "domain": domain,
        "api_key": HUNTER_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"].get("email"):
            email = data["data"]["email"]
            confidence = data["data"].get("score", "N/A")
            print(f"\n✅ Found Email: {email} (Confidence: {confidence})")
            return email
        else:
            print("\n❌ No email found for this person.")
    else:
        print(f"\n⚠️ API Error: {response.status_code} - {response.text}")
    return None

def main():
    print("=== Hunter.io Email Finder ===")
    name = input("Enter the person's full name: ").strip()
    organization = input("Enter the organization/company name: ").strip()

    domain = get_domain_from_organization(organization)
    if domain:
        find_email(name, domain)

if __name__ == "__main__":
    main()
