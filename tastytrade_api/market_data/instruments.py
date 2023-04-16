import requests
import json
from typing import List
import urllib

class TastytradeInstruments:
    """
    Implements the Tastytrade Instruments API - https://developer.tastytrade.com/open-api-spec/instruments/
    """

    def __init__(self, session_token: str, api_url: str):
        self.session_token = session_token
        self.api_url = api_url

    def get_cryptocurrencies(self, symbols: List[str] = None) -> List[dict]:
        """
        Makes a GET request to the /instruments/cryptocurrencies API endpoint for the specified cryptocurrency symbols,
        and returns a list of cryptocurrency objects.

        :param symbols: Optional. A list of cryptocurrency symbols to retrieve. If not provided, all cryptocurrencies will be returned.
        :type symbols: List[str]
        :return: A list of dictionaries, where each dictionary represents a cryptocurrency.
        :rtype: List[dict]

        :raises: Exception if there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        if symbols:
            symbol_params = "&".join([f"symbol[]={s}" for s in symbols])
            url = f"{self.api_url}/instruments/cryptocurrencies?{symbol_params}"
        else:
            url = f"{self.api_url}/instruments/cryptocurrencies"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            cryptocurrencies = response_data["data"]["items"]
            return cryptocurrencies
        else:
            raise Exception(f"Error getting cryptocurrencies: {response.status_code} - {response.content}")

    def get_cryptocurrency_by_symbol(self, symbol: str) -> dict:
        """
        Returns the cryptocurrency object for the given symbol.

        :param symbol: The symbol of the cryptocurrency to retrieve.
        :type symbol: str
        :return: A dictionary representing the cryptocurrency object.
        :rtype: dict
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        response = requests.get(f"{self.api_url}/instruments/cryptocurrencies/{symbol}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting cryptocurrency '{symbol}': {response.status_code} - {response.content}")

    def get_active_equities(self, per_page: int = 1000, page_offset: int = 0, lendability: str = None) -> List[dict]:
        """
        Returns a list of all active equities in a paginated fashion.

        :param per_page: Optional. The number of equities to return per page. Default is 1000.
        :type per_page: int
        :param page_offset: Optional. The page number to start the results from. Default is 0.
        :type page_offset: int
        :param lendability: Optional. The lendability type of the equities. Valid options are "Easy To Borrow",
                            "Locate Required", and "Preborrow". Default is None, which returns all lendability types.
        :type lendability: str
        :return: A list of dictionaries, where each dictionary represents an equity.
        :rtype: List[dict]
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        params = {"per-page": per_page, "page-offset": page_offset}
        if lendability:
            params["lendability"] = lendability

        response = requests.get(f"{self.api_url}/instruments/equities/active", headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error getting active equities with status {response.status_code} - {response.content}")
        return response.json()
    
    def get_equities(self, symbols=None, lendability=None, is_index=None, is_etf=None):
        """
        Makes a GET request to the /instruments/equities API endpoint for the specified equity symbols,
        and returns a list of equity objects.

        Args:
            symbols (Union[str, List[str]]): A single equity symbol or a list of equity symbols. If a single symbol is 
                passed, the /instruments/equities/{symbol} endpoint will be used. If a list is passed, the 
                /instruments/equities/ endpoint will be used.
            lendability (str): Optional. The lendability type of the equities. Valid options are "Easy To Borrow",
                            "Locate Required", and "Preborrow". Default is None, which returns all lendability types.
            is_index (bool): Optional. Flag indicating if equity is an index instrument. Default is None, which means
                            the filter is not applied.
            is_etf (bool): Optional. Flag indicating if equity is an ETF instrument. Default is None, which means
                            the filter is not applied.

        Returns:
            list: List of equity objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }
        
        if isinstance(symbols, str): 
            params = {"symbol": symbols}
            response = requests.get(f"{self.api_url}/instruments/equities/", headers=headers, params=params)
        else:
    
            params = {}
            if symbols:
                params["symbol[]"] = symbols
            if lendability:
                params["lendability"] = lendability
            if is_index is not None:
                params["is-index"] = is_index
            if is_etf is not None:
                params["is-etf"] = is_etf
            
            url = f"{self.api_url}/instruments/equities"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            response = requests.get(full_url, headers=headers, params=params)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            equities = response_data["data"]["items"]
            return equities
        else:
            raise Exception(f"Error getting equities: {response.status_code} - {response.content}")


    def get_equity_options(self, symbols=None, active=None, with_expired=None):
        """
        Makes a GET request to the /instruments/equity-options API endpoint for the specified equity option symbols,
        and returns a list of equity option objects.

        Args:
            symbols (Union[str, List[str]]): A single equity option symbol or a list of equity option symbols. If a single symbol is 
                passed, the /instruments/equity-options/{symbol} endpoint will be used. If a list is passed, the 
                /instruments/equity-options/ endpoint will be used.
            active (bool): Optional. Flag indicating if equity option is currently available for trading with the broker.
                            Default is None, which means the filter is not applied.
            with_expired (bool): Optional. Flag indicating if expired equity options should be included in the response.
                                Default is None, which means the filter is not applied.

        Returns:
            list: List of equity option objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        if isinstance(symbols, str): 
            params = {"symbol": symbols}
            response = requests.get(f"{self.api_url}/instruments/equity-options/", headers=headers, params=params)
        else:
            params = {}
            if symbols:
                params["symbol[]"] = symbols
            if active is not None:
                params["active"] = active
            if with_expired is not None:
                params["with-expired"] = with_expired
            
            url = f"{self.api_url}/instruments/equity-options"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            equity_options = response_data["data"]["items"]
            return equity_options
        else:
            raise Exception(f"Error getting equity options: {response.status_code} - {response.content}")

    def get_equity_options(self, symbols=None, active=None, with_expired=None):
        """
        Makes a GET request to the /instruments/equity-options API endpoint for the specified equity option symbols,
        and returns a list of equity option objects.

        Args:
            symbols (Union[str, List[str]]): A single equity option symbol or a list of equity option symbols. If a single symbol is 
                passed, the /instruments/equity-options/{symbol} endpoint will be used. If a list is passed, the 
                /instruments/equity-options/ endpoint will be used.
            active (bool): Optional. Flag indicating if equity option is currently available for trading with the broker.
                            Default is None, which means the filter is not applied.
            with_expired (bool): Optional. Flag indicating if expired equity options should be included in the response.
                                Default is None, which means the filter is not applied.

        Returns:
            list: List of equity option objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        if isinstance(symbols, str): 
            params = {"symbol": symbols}
            print(params)
            response = requests.get(f"{self.api_url}/instruments/equity-options", headers=headers, params=params)
        else:
            params = {}
            if symbols:
                params["symbol[]"] = symbols
            if active is not None:
                params["active"] = active
            if with_expired is not None:
                params["with-expired"] = with_expired         
            url = f"{self.api_url}/instruments/equity-options"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            print(full_url)
            
            response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            equity_options = response_data["data"]["items"]
            return equity_options
        else:
            raise Exception(f"Error getting equity options: {response.status_code} - {response.content}")

    def get_futures(self, symbols=None, product_codes=None):
        """
        Makes a GET request to the /instruments/futures API endpoint for the specified futures symbols or product codes,
        and returns a list of future objects.

        Args:
            symbols (Union[str, List[str]]): A single future symbol or a list of future symbols. If a single symbol is 
                passed, the /instruments/futures/{symbol} endpoint will be used. If a list is passed, the 
                /instruments/futures/ endpoint will be used.
            product_codes (Union[str, List[str]]): A single product code or a list of product codes. If a single product code is 
                passed, the /instruments/futures?product-code={product_code} endpoint will be used. If a list is passed, the 
                /instruments/futures/ endpoint will be used.

        Returns:
            list: List of future objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        if isinstance(symbols, str):
            params = {"symbol[]": symbols}
        elif isinstance(symbols, list):
            params = {"symbol[]": symbols}
        else:
            params = {}

        if isinstance(product_codes, str):
            params["product-code[]"] = product_codes
        elif isinstance(product_codes, list):
            params["product-code[]"] = product_codes

        url = f"{self.api_url}/instruments/futures"
        query_string = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{url}?{query_string}"
        print(full_url)

        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            futures = response_data["data"]["items"]
            return futures
        else:
            raise Exception(f"Error getting futures: {response.status_code} - {response.content}")

    def get_future_option_products(self):
        """
        Makes a GET request to the /instruments/future-option-products API endpoint and returns metadata for all supported
        future option products.

        Returns:
            list: List of future option product objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        response = requests.get(f"{self.api_url}/instruments/future-option-products", headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            future_option_products = response_data["data"]["items"]
            return future_option_products
        else:
            raise Exception(f"Error getting future option products: {response.status_code} - {response.content}")
    
    """
    TBD: Get a future option product by exchange and root symbol 
    /instruments/future-option-products/{exchange}/{root_symbol}
    """
    
    """
    TBD: Get a future option product by exchange and root symbol
    /instruments/future-option-products/{exchange}/{root_symbol}
    """ 
    
    """
    TBD: /instruments/future-options and /instruments/future-options/{symbol}
        Returns a set of future option(s) given an array of one or more symbols.
    """
    def get_future_products(self):
        """
        Makes a GET request to the /instruments/future-products API endpoint and returns metadata for all supported
        futures products.

        Returns:
            list: List of future product objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        response = requests.get(f"{self.api_url}/instruments/future-products", headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            future_products = response_data["data"]["items"]
            return future_products
        else:
            raise Exception(f"Error getting future products: {response.status_code} - {response.content}")

    def get_quantity_decimal_precisions(self):
        """
        Makes a GET request to the /instruments/quantity-decimal-precisions API endpoint and retrieves all quantity decimal
        precisions.

        Returns:
            dict: Dictionary containing the quantity decimal precision for each supported instrument type, as returned by
            the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        headers = {
            "Authorization": f"{self.session_token}"
        }

        response = requests.get(f"{self.api_url}/instruments/quantity-decimal-precisions", headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            quantity_decimal_precisions = response_data["data"]
            return quantity_decimal_precisions
        else:
            raise Exception(f"Error getting quantity decimal precisions: {response.status_code} - {response.content}")

    """
    TBD: /instruments/warrants and /instruments/warrants/{symbol}
    Returns a set of warrant definitions that can be filtered by parameters
    """
    
    """
    TBD: Future options chanins and option chains implementation
    """


