import requests
import json

class TastytradeAccount:
    def __init__(self, session_token, api_url):
        self.session_token = session_token
        self.api_url = api_url

    def get_accounts(self):
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/customers/me/accounts", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            accounts = response_data["data"]["items"]
            return accounts
        else:
            raise Exception(f"Error getting accounts: {response.status_code} - {response.content}")
'''
session_token = "your_token"
api_url = "https://api.tastytrade.com"

account = TastytradeAccount(session_token, api_url)
accounts = account.get_accounts()

print(accounts)
'''