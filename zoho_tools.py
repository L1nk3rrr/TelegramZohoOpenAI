import os
import requests

ZOHO_API_TOKEN_URL = "https://accounts.zoho.eu/oauth/v2/token"
ZOHO_API_CRM_URL = "https://www.zohoapis.eu/crm/v2/Leads"


def get_refresh_token():
    body = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "code": os.getenv("ZOHO_CLIENT_CODE"),
    }
    response = requests.post(ZOHO_API_TOKEN_URL, params=body)
    return response.json()


def get_access_token():
    data = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
    }
    # Send the request to the Zoho token endpoint
    token_response = requests.post(ZOHO_API_TOKEN_URL, data=data)
    return token_response.json().get("access_token")


def make_zoho_api_get_request(endpoint):
    zoho_token = get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()
