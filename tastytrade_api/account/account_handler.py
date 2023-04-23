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
        
    def get_margin_requirements(self, account_number):
        """
        Makes a GET request to the /margin/accounts/{account_number}/requirements API endpoint for the specified account's 
        margin/capital requirements report, and returns the report object.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            dict: Dictionary containing the margin/capital requirements report, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/margin/accounts/{account_number}/requirements", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            report = response_data["data"]
            return report
        else:
            raise Exception(f"Error getting margin requirements for account {account_number}: {response.status_code} - {response.content}")

    def get_account_net_liq_history(self, account_number: str, time_back: str = None, start_time: str = None) -> dict:
        """
        Makes a GET request to the /accounts/{account_number}/net-liq/history endpoint with the specified
        parameters, and returns the response as a JSON object.

        Args:
            account_number (str): The account number for the account to retrieve net liq history.
            
            time_back (str): The duration of time to retrieve net liq history for. If given, will return data for a specific
            period of time with a pre-defined time interval. Passing 1d will return the previous day of data in 5 minute 
            intervals. This param is required if start-time is not given. 
            1d - If equities market is open, this will return data starting from market open in 5 minute intervals.
            If market is closed, will return data from previous market open.
            
            start_time (str): The starting datetime to retrieve net liq history from.
            This param is required is time-back is not given.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        params = {
            "time-back": time_back,
            "start-time": start_time
        }
        response = requests.get(f"{self.api_url}/accounts/{account_number}/net-liq/history", headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting account net liq history: {response.status_code} - {response.content}")

    def get_effective_margin_requirements(self, account_number, underlying_symbol):
        """
        This method is similar to the get_margin_requirements method, except that it retrieves the effective margin 
        requirements for a specific underlying symbol rather than the overall margin/capital requirements report.
        
        Makes a GET request to the /accounts/{account_number}/margin-requirements/{underlying_symbol}/effective endpoint
        for the specified account's effective margin requirements for the given underlying symbol, and returns the response
        as a JSON object.

        Args:
            account_number (str): The account number for the account to retrieve effective margin requirements for.
            underlying_symbol (str): The underlying symbol for which to retrieve effective margin requirements.

        Returns:
            dict: Dictionary containing the effective margin requirements, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(
            f"{self.api_url}/accounts/{account_number}/margin-requirements/{underlying_symbol}/effective",
            headers=headers
        )
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting effective margin requirements for account {account_number}: "
                            f"{response.status_code} - {response.content}")

    def get_position_limit(self, account_number):
        """
        Makes a GET request to the /accounts/{account_number}/position-limit API endpoint for the specified account's
        position limit, and returns the position limit.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            int: The position limit for the account, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/accounts/{account_number}/position-limit", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            position_limit = response_data["data"]["positionLimit"]
            return position_limit
        else:
            raise Exception(f"Error getting position limit for account {account_number}: {response.status_code} - {response.content}")