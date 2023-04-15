import requests
import json

class TastytradeAccount:
    """
    Initializes a new instance of the API client with the given session token and API URL.

    Args:
        session_token (str): The session token used to authenticate API requests.
        api_url (str): The base URL of the API.

    Returns:
        None
    """
    def __init__(self, session_token, api_url):
        self.session_token = session_token
        self.api_url = api_url

    def get_accounts(self):
        """
        Makes a GET request to the /customers/me/accounts API endpoint for the authenticated customer's accounts,
        and returns a list of account objects.

        Returns:
            list: List of account objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
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
        
    def get_customer(self):
        """
        Makes a GET request to the /customers/{customer_id} API endpoint for a specific customer,
        and returns the customer object.

        Returns:
            dict: The customer object, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/customers/me", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            customer = response_data["data"]
            return customer
        else:
            raise Exception(f"Error getting customer: {response.status_code} - {response.content}")
        
    def get_customer_account(self, account_number):
        """
        Makes a GET request to the /customers/me/accounts/{account_number} API endpoint for the authenticated customer's 
        account details, and returns the account object.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            dict: Dictionary containing the account details, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/customers/me/accounts/{account_number}", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            account = response_data["data"]
            return account
        else:
            raise Exception(f"Error getting account {account_number}: {response.status_code} - {response.content}")