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
        Returns an array of volatility data for given symbols.

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
    
    def get_dividend_data(self, symbol):
        """
        Get historical dividend data

        Makes a GET request to the /market-metrics/historic-corporate-events/dividends/{symbol} endpoint with the specified symbol as a path parameter,
        and returns the response as a JSON object.

        Args:
            symbol (str): Symbol to get dividends data for.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        response = requests.get(f"{self.api_url}/market-metrics/historic-corporate-events/dividends/{symbol}", headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting dividend data for symbol {symbol}: {response.status_code} - {response.content}")


    def get_earnings_data(self, symbol: str, start_date: str = None) -> dict:
        """
        Makes a GET request to the /market-metrics/historic-corporate-events/earnings-reports/{symbol} endpoint
        for the specified symbol's earnings data, and returns the response as a JSON object.

        Args:
            symbol (str): The symbol to query.
            start_date (str, optional): The start date to limit earnings data from. Format is YYYY-MM-DD.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        url = f"{self.api_url}/market-metrics/historic-corporate-events/earnings-reports/{symbol}"
        if start_date:
            url += f"?start-date={start_date}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting earnings data for {symbol}: {response.status_code} - {response.content}")

