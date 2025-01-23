import requests

def generate_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        return None

# Example usage
if __name__ == "__main__":
    api_key = input("Enter your API key: ")
    token = generate_access_token(api_key)
    if token:
        print(f"Generated Access Token: {token}")
    else:
        print("Failed to generate access token.")
