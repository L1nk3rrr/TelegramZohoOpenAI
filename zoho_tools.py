import aiohttp

import os

ZOHO_API_TOKEN_URL = "https://accounts.zoho.eu/oauth/v2/token"
ZOHO_API_CRM_URL = "https://www.zohoapis.eu/crm/v2/Leads"


async def get_refresh_token():
    body = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "code": os.getenv("ZOHO_CLIENT_CODE"),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(ZOHO_API_TOKEN_URL, params=body) as response:
            response_data = await response.json()
            return response_data.json()


async def get_access_token():
    data = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
    }
    # Send the request to the Zoho token endpoint
    async with aiohttp.ClientSession() as session:
        async with session.post(ZOHO_API_TOKEN_URL, data=data) as response:
            response_data = await response.json()
            return response_data.get("access_token")


async def make_zoho_api_get_request(endpoint):
    zoho_token = await get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers) as response:
            response_data = await response.json()
            return response_data.json()


async def make_zoho_api_post_request(endpoint: str, data: dict):
    zoho_token = await get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=data, headers=headers) as response:
            response_data = await response.json()
            return response_data


async def create_lead(user_data: dict):
    payload = {
        "data": [
            {
                "First_Name": user_data.get("name"),
                "Last_Name": "User",
                "Email": user_data.get("email"),
                "City": user_data.get("city"),
                "Feedback": user_data.get("feedback"),
                "Sentiment": user_data.get("sentiment"),
                "Description": "User feedback",
            }
        ]
    }
    return await make_zoho_api_post_request(ZOHO_API_CRM_URL, payload)
