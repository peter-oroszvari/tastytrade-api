import requests
import json

class TastytradeWatchlist:

    def __init__(self, session_token: str = None, api_url: str = 'https://api.tastytrade.com/'):
        self.api_url = api_url
        self.session_token = session_token
        self.headers = {
            "Authorization": f"{self.session_token}"
        }

    def get_pairs_watchlists(self, pairs_watchlist_name: str = None):
        """
        Returns a list of all tastyworks pairs watchlists if paries_watchlist_name is not provided (None)
        Returns a requested tastyworks pairs watchlist if pairs_watchlist_name is provided

        Retrieves the pairs watchlists from the API. If `pairs_watchlist_name` is provided, retrieves the watchlist
        with that name. If not, retrieves all pairs watchlists.

        Args:
            pairs_watchlist_name (str): (optional) The name of the pairs watchlist to retrieve.

        Returns:
            dict: The response data containing the pairs watchlists.

        Raises:
            Exception: If there was an error retrieving the pairs watchlists.
        """
        if pairs_watchlist_name is None:
            url = f"{self.api_url}/pairs-watchlists"
        else:
            url = f"{self.api_url}/pairs-watchlists/{pairs_watchlist_name}"
        
        response = requests.get(url, headers=self.headers)
    
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting pairs watchlists: {response.status_code} - {response.content}")

    def get_public_watchlists(self, counts_only: bool = False):
        """
        Returns a list of all tastyworks pairs watchlists
        Get the public watchlists from the API.

        Args:
            counts_only (bool): Whether to only return the counts of the watchlists.

        Returns:
            dict: A dictionary containing the response data.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.api_url}/public-watchlists"
        if counts_only:
            url += "?counts-only=true"
        
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting public watchlists: {response.status_code} - {response.content}")
        
    def get_public_watchlist(self, watchlist_name: str):
        """
        Returns a requested tastyworks pairs watchlist
        Get the content of a public watchlist by its name.

        Args:
            watchlist_name (str): The name of the public watchlist.

        Returns:
            dict: A dictionary containing the content of the watchlist.

        Raises:
            Exception: If the HTTP response status code is not 200.
        """
    
        url = f"{self.api_url}/public-watchlists/{watchlist_name}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting public watchlist: {response.status_code} - {response.content}")
        
    def create_account_watchlist(self, watchlist_data):
        """
        Creates an account watchlist.

        Args:
            watchlist_data (dict): The data for the new watchlist, including the name, group name, order index, and a list of watchlist entries.

        Returns:
            dict: The watchlist data, including the watchlist ID and watchlist entries.

        Example:
            >>> new_watchlist_data = {
            ...     "name": "my_new_watchlist",
            ...     "group-name": "my_group",
            ...     "order-index": 9999,
            ...     "watchlist-entries": [
            ...         {
            ...             "symbol": "AAPL",
            ...             "instrument-type": "EQUITY"
            ...         },
            ...         {
            ...             "symbol": "GOOGL",
            ...             "instrument-type": "EQUITY"
            ...         },
            ...         {
            ...             "symbol": "TSLA",
            ...             "instrument-type": "EQUITY"
            ...         }
            ...     ]
            ... }
        """
        url = f"{self.api_url}/watchlists"
        payload = json.dumps(watchlist_data)
        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error creating account watchlist: {response.status_code} - {response.content}")
    
    def get_account_watchlists(self, watchlist_name: str = None):
        """
        Returns a list of all watchlists for the given account, or a requested watchlist if a watchlist name is specified.
        Sends a GET request to retrieve the watchlists data for the authenticated account.

        Args:
            watchlist_name (str, optional): The name of the watchlist to retrieve. Defaults to None.

        Returns:
            A dictionary containing the watchlists data, or the data for a requested watchlist, as returned by the API.

        Raises:
            Exception: If the request fails or returns a non-200 status code.
        """
        if watchlist_name is None:
            url = f"{self.api_url}/watchlists"
        else:
            url = f"{self.api_url}/watchlists/{watchlist_name}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting account watchlists: {response.status_code} - {response.content}")
    def update_account_watchlist(self, watchlist_name: str, watchlist_data):
        """
        Replace all properties of an account watchlist

        Args:
            watchlist_name (str): The name of the watchlist to update.
            watchlist_data (dict): The updated data for the watchlist, including the name, group name, order index, and a list of watchlist entries.

        Returns:
            dict: The updated watchlist data, including the watchlist ID and watchlist entries.
        """
        url = f"{self.api_url}/watchlists/{watchlist_name}"
        payload = json.dumps(watchlist_data)
        response = requests.put(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error updating account watchlist: {response.status_code} - {response.content}")
    def delete_account_watchlist(self, watchlist_name: str):
        """
        Deletes a watchlist for the given account.

        Args:
            watchlist_name (str): The name of the watchlist to delete.

        Returns:
            dict: An empty dictionary, indicating that the watchlist was successfully deleted.

        """
        url = f"{self.api_url}/watchlists/{watchlist_name}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            return {}
        else:
            raise Exception(f"Error deleting account watchlist: {response.status_code} - {response.content}")