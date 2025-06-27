import requests
import json

# API URL for the OAuth and API endpoints for connection
TOKEN_URL = "https://mbn-provider.authentication.eu12.hana.ondemand.com/oauth/token"
API_URL = "https://interview-demo-transport-backend.cfapps.eu12.hana.ondemand.com/transports"

# Client credentials for connecting
CLIENT_ID = "sb-interview_demo_transport_app!b923597"
CLIENT_SECRET = "e5a58e12-6849-4833-8800-5eee585f347c$H0EkGqSXYJXVJTOMOocIcfufzbPmpeastGoMvrbKfIQ="
SCOPE = "interview_demo_transport_app!b923597.transportread"

def get_token():
    "Get the OAuth token from the authorization server."
    payload = {
        "grant_type": "client_credentials",
        "response_type": "token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()  # Will raise  errors, exception for HTTP

    token_data = response.json()
    return token_data["access_token"]

def fetch_transports(token):
    "Using the token to fetch transport data's from  API."
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()

    return response.json()

def print_transport_details(transports):
    "Print selected fields from each transport entry."
    for transport in transports:
        print(f"ID: {transport['id']}")
        print(f"Description: {transport['description']}")
        print(f"Type: {transport['type']}")
        print(f"Start Timestamp: {transport['starttimestamp']}")
        print(f"End Timestamp: {transport['endtimestamp']}")
        print("-" * 40)

def main():
    try:
        token = get_token()
        transports = fetch_transports(token)
        print_transport_details(transports)
    except requests.RequestException as e:
        print("Error during request:", e)
    except KeyError:
        print("Error parsing token or response")

if __name__ == "__main__":
    main()