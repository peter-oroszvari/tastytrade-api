import requests
import json

class TastytradeOrder:
    def __init__(self, session_token: str = None, api_url: str = 'https://api.tastytrade.com/accounts'):
        self.api_url = api_url
        self.session_token = session_token
        self.headers = {
            "Authorization": f"{self.session_token}"
        }

        
    
    def reconfirm_order(self, account_number, order_id):
        """
        Makes a POST request to the /accounts/{account_number}/orders/{order_id}/reconfirm API endpoint to reconfirm an order,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to reconfirm.
            order_id (int): The ID of the order to reconfirm.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}/reconfirm"
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error reconfirming order: {response.status_code} - {response.content}")
    
    def dry_run_order(self, account_number, order_id, order_data):
        """
        Runs through preflights for cancel-replace and edit without routing
        
        Makes a POST request to the /accounts/{account_number}/orders/{order_id}/dry-run API endpoint to run preflights for cancel-replace and edit without routing,
        and returns the response as a JSON object. 

        Args:
            account_number (int): The account number for the order to run preflights on.
            order_id (int): The ID of the order to run preflights on.
            order_data (dict): Dictionary containing the order data to use for the preflight.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}/dry-run"
        response = requests.post(url, headers=self.headers, json=order_data)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error running dry run order: {response.status_code} - {response.content}")

    def get_order(self, account_number, order_id):
        """
        Returns a single order based on the id
        
        Makes a GET request to the /accounts/{account_number}/orders/{order_id} API endpoint to get a single order based on its ID,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to retrieve.
            order_id (int): The ID of the order to retrieve.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting order: {response.status_code} - {response.content}")
        
    def cancel_order(self, account_number, order_id):
        """
        Requests order cancellation

        Makes a DELETE request to the /accounts/{account_number}/orders/{order_id} API endpoint to request order cancellation,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to cancel.
            order_id (int): The ID of the order to cancel.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the DELETE request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error cancelling order: {response.status_code} - {response.content}")
        
    def replace_order(self, account_number, order_id, order_data):
        """
        Replaces a live order with a new one. Subsequent fills of the original order will abort the replacement.

        Makes a PUT request to the /accounts/{account_number}/orders/{order_id} API endpoint to replace a live order with a new one,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to replace.
            order_id (int): The ID of the order to replace.
            order_data (dict): Dictionary containing the order data to use for the replacement.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the PUT request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.put(url, headers=self.headers, json=order_data)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error replacing order: {response.status_code} - {response.content}")

    def edit_order(self, account_number, order_id, order_data):
        """
        Edit price and execution properties of a live order by replacement. Subsequent fills of the original order
        
        Makes a PATCH request to the /accounts/{account_number}/orders/{order_id} API endpoint to edit price and execution properties of a live order by replacement,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to edit.
            order_id (int): The ID of the order to edit.
            order_data (dict): Dictionary containing the updated order data to use for the replacement.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the PATCH request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.patch(url, headers=self.headers, json=order_data)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error editing order: {response.status_code} - {response.content}")
        
    def get_live_orders(self, account_number):
        """
        Returns a list of live orders for the resource


        Makes a GET request to the /accounts/{account_number}/orders/live API endpoint to retrieve a list of live orders,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to retrieve the list of live orders.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/live"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting live orders: {response.status_code} - {response.content}")
        
    def get_orders(self, account_number, per_page=10, page_offset=0, start_date=None, end_date=None, underlying_symbol=None, 
                   status=None, futures_symbol=None, underlying_instrument_type=None, sort='Desc', start_at=None, end_at=None):
        """
        Returns a paginated list of the customer's orders (as identified by the provided authentication token)
        based on sort param. If no sort is passed in, it defaults to descending order.
        
        Makes a GET request to the /accounts/{account_number}/orders API endpoint to retrieve a paginated list of the customer's orders
        based on the provided parameters, and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to retrieve the list of orders.
            per_page (int): The number of orders to return per page.
            page_offset (int): The page offset to use when retrieving orders.
            start_date (str): The start date to use for filtering orders.
            end_date (str): The end date to use for filtering orders.
            underlying_symbol (str): The underlying symbol to use for filtering orders.
            status (list): The status values to use for filtering orders.
            futures_symbol (str): The futures symbol to use for filtering orders.
            underlying_instrument_type (str): The underlying instrument type to use for filtering orders.
            sort (str): The order to sort results in. Accepts 'Desc' or 'Asc'. Defaults to 'Desc'.
            start_at (str): The start date and time to use for filtering orders in full date-time.
            end_at (str): The end date and time to use for filtering orders in full date-time.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders"
        params = {
            "per-page": per_page,
            "page-offset": page_offset,
            "start-date": start_date,
            "end-date": end_date,
            "underlying-symbol": underlying_symbol,
            "status[]": status,
            "futures-symbol": futures_symbol,
            "underlying-instrument-type": underlying_instrument_type,
            "sort": sort,
            "start-at": start_at,
            "end-at": end_at
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting orders: {response.status_code} - {response.content}")
        
    def create_order(self, account_number, order):
        """
        Accepts a json document containing parameters to create an order for the client.

        Makes a POST request to the /accounts/{account_number}/orders API endpoint to create a new order for the customer,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to create the order.
            order (dict): The order details to be created.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 CREATED.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders"
        headers = {
            "Authorization": f"{self.session_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=order)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error creating order: {response.status_code} - {response.content}")
        
    def dry_run_new_order(self, account_number, order_data):
        """
        Accepts a json document containing parameters to create an order and then runs the preflights without placing the order.

        Makes a POST request to the /accounts/{account_number}/orders/dry-run API endpoint to validate a new order without placing it, 
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the new order.
            order_data (dict): Dictionary containing the order data to use for validation.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/dry-run"
        response = requests.post(url, headers=self.headers, json=order_data)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error running dry run new order: {response.status_code} - {response.content}")

    def get_customer_live_orders(self, customer_id):
        """
        Returns a list of live orders for the customer.

        Makes a GET request to the /customers/{customer_id}/orders/live API endpoint to retrieve a list of live orders for the customer,
        and returns the response as a JSON object.

        Args:
            customer_id (int): The ID of the customer for which to retrieve live orders.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/customers/{customer_id}/orders/live"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting live orders for customer {customer_id}: {response.status_code} - {response.content}")
        
    def get_customer_orders(self, customer_id, per_page=10, page_offset=0, start_date=None, end_date=None,
                             underlying_symbol=None, status=None, futures_symbol=None, underlying_instrument_type=None,
                             sort='Desc', start_at=None, end_at=None):
        """
        Returns a paginated list of the customer's orders based on sort param. 
        If no sort is passed in, it defaults to descending order.
        
        Makes a GET request to the /customers/{customer_id}/orders API endpoint for the authenticated customer's orders,
        and returns a paginated list of the orders.

        Args:
            customer_id (int): The ID of the customer whose orders to retrieve.
            per_page (int): The number of orders to retrieve per page.
            page_offset (int): The page offset to retrieve (e.g. 0 for the first page, 10 for the second, etc.).
            start_date (str): The start date to filter orders by (in yyyy-mm-dd format).
            end_date (str): The end date to filter orders by (in yyyy-mm-dd format).
            underlying_symbol (str): The underlying symbol to filter orders by.
            status (list[str]): A list of order statuses to filter by (e.g. ['Filled', 'Working']).
            futures_symbol (str): The futures symbol to filter orders by.
            underlying_instrument_type (str): The underlying instrument type to filter orders by.
            sort (str): The order to sort results in. Accepts 'Desc' or 'Asc'. Defaults to 'Desc'.
            start_at (str): DateTime start range for filtering orders in full date-time.
            end_at (str): DateTime end range for filtering orders in full date-time.

        Returns:
            list: List of order objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/customers/{customer_id}/orders"
        params = {
            "per-page": per_page,
            "page-offset": page_offset,
            "start-date": start_date,
            "end-date": end_date,
            "underlying-symbol": underlying_symbol,
            "status[]": status,
            "futures-symbol": futures_symbol,
            "underlying-instrument-type": underlying_instrument_type,
            "sort": sort,
            "start-at": start_at,
            "end-at": end_at
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            orders = response_data["data"]["items"]
            return orders
        else:
            raise Exception(f"Error getting customer orders: {response.status_code} - {response.content}")