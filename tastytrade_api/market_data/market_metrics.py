import requests
from typing import List

class MarketMetrics():
    """
    Initializes a new instance of the MarketMetrics client with the given session token and API URL.

    Args:
        session_token (str): The session token used to authenticate API requests.
        api_url (str): The base URL of the API.

    Returns:
        None
    """
    def __init__(self, session_token, api_url):
        self.session_token = session_token
        self.api_url = api_url

    def get_metrics(self, symbols: List[str]) -> dict:
        """
        Makes a GET request to the /market-metrics endpoint with the specified symbols as a query parameter, and returns the response as a JSON object.

        Args:
            symbols (list): List of symbols to query.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        params = {
            "symbols": ",".join(symbols)
        }
        response = requests.get(f"{self.api_url}/market-metrics", headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting market metrics: {response.status_code} - {response.content}")
