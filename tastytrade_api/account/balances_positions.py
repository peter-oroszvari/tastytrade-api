import requests
import json

class TastytradeAccountPositions:
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

    def get_positions(self, account_number, underlying_symbol=None, symbol=None, instrument_type=None, include_closed_positions=False, underlying_product_code=None, partition_keys=None, net_positions=False, include_marks=False):
        """
        Makes a GET request to the /accounts/{account_number}/positions API endpoint for the specified account's positions,
        and returns a list of position objects.

        Args:
            account_number (int): The account number to retrieve positions for.
            underlying_symbol (list of str, optional): An array of underlying symbols to filter positions by. Defaults to None.
            symbol (str, optional): A single symbol to filter positions by. Defaults to None.
            instrument_type (str, optional): The type of instrument to filter positions by. Defaults to None.
            include_closed_positions (bool, optional): Whether to include closed positions in the query. Defaults to False.
            underlying_product_code (str, optional): The underlying future's product code to filter positions by. Defaults to None.
            partition_keys (list of str, optional): Account partition keys. Defaults to None.
            net_positions (bool, optional): Whether to return net positions grouped by instrument type and symbol. Defaults to False.
            include_marks (bool, optional): Whether to include current quote marks. Defaults to False.

        Returns:
            list: List of position objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        params = {
            "underlying-symbol": underlying_symbol,
            "symbol": symbol,
            "instrument-type": instrument_type,
            "include-closed-positions": include_closed_positions,
            "underlying-product-code": underlying_product_code,
            "partition-keys": partition_keys,
            "net-positions": net_positions,
            "include-marks": include_marks,
        }
        response = requests.get(f"{self.api_url}/accounts/{account_number}/positions", headers=headers, params=params)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            positions = response_data["data"]["items"]
            return positions
        else:
            raise Exception(f"Error getting positions: {response.status_code} - {response.content}")

    def get_account_balances(self, account_number):
        """
        Makes a GET request to the /accounts/{account_number}/balances API endpoint for the account's balances,
        and returns a dictionary of balance values.

        Args:
            account_number (int): The account number for which to retrieve balances.

        Returns:
            dict: Dictionary of balance values, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/accounts/{account_number}/balances", headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            balances = response_data["data"]
            return balances
        else:
            raise Exception(f"Error getting account balances: {response.status_code} - {response.content}")
    def get_balance_snapshots(self, account_number, snapshot_date=None, time_of_day="EOD"):
        """
        Makes a GET request to the /accounts/{account_number}/balance-snapshots API endpoint for the specified account's
        balance snapshots, and returns the most recent snapshot and current balance.

        Args:
            account_number (int): The account number for which to retrieve balance snapshots.
            snapshot_date (str): The day of the balance snapshot to retrieve, in YYYY-MM-DD format.
            time_of_day (str): The abbreviation for the time of day. Available values: "EOD" (End of Day), "BOD" (Beginning of Day).

        Returns:
            dict: The most recent snapshot and current balance, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        params = {
            "snapshot-date": snapshot_date,
            "time-of-day": time_of_day
        }
        response = requests.get(f"{self.api_url}/accounts/{account_number}/balance-snapshots", headers=headers, params=params)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            return response_data
        else:
            raise Exception(f"Error getting balance snapshots: {response.status_code} - {response.content}")
