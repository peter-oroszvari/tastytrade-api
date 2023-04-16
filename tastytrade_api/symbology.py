def to_tastytrade_option_symbol(symbol: str, strike_price: float, option_type: str, expiration_date: str) -> str:
    """
    Generate Tastytrade option symbol based on input parameters.

    Args:
        symbol (str): Ticker symbol for the underlying asset.
        strike_price (float): Strike price of the option.
        option_type (str): Type of option, either "call" or "put".
        expiration_date (str): Expiration date of the option in yyyy-mm-dd format.

    Returns:
        str: Tastytrade option symbol in the format "SYMBOLYYMMDDTXXXXXP/C".

    Example:
        >>> to_tastytrade_option_symbol("AAPL", 130.0, "call", "2022-01-21")
        "AAPL  220121C00130000"
    """
 
    # convert strike price to 8-digit integer (multiply by 1000 and convert to int)
    strike_price_int = int(strike_price * 1000)
    
    # format expiration date to yymmdd format
    expiration_date_formatted = expiration_date[2:].replace('-', '')
    
    # format option type to P or C
    option_type_formatted = option_type[0].upper()
    
    # pad symbol with whitespace to 6 characters
    symbol_padded = symbol.ljust(6)
    
    # combine all parts to form Tastytrade option symbol
    option_symbol = f"{symbol_padded}{expiration_date_formatted}{option_type_formatted}{strike_price_int:08d}"
    
    return option_symbol

def to_tastytrade_future_symbol(product_code: str, expiration_date: str) -> str:
    """
    Generate Tastytrade futures symbol based on input parameters.

    Args:
        product_code (str): Product code for the futures symbol (e.g. "CL" for crude oil).
        expiration_date (str): Expiration date of the futures contract in yyyy-mm format.

    Returns:
        str: Tastytrade futures symbol in the format "/PRODUCTCODEYYMM".

    Example:
        >>> to_tastytrade_future_symbol("CL", "2022-12")
        "/CLZ22"
    """
    year, month = expiration_date.split('-')
    month_codes = "FGHJKMNQUVXZ"
    month_code = month_codes[int(month)-1]
    last_digit_of_year = year[-1]

    # Combine the product code, month code, and year code to form the Tastytrade future symbol
    future_symbol = f"/{product_code}{month_code}{last_digit_of_year}"

    return future_symbol

def to_tastytrade_future_option_symbol(symbol: str, future_month: str, option_product_code: str, expiration_date: str, option_type: str, strike_price: float) -> str:
    """
    Generate Tastytrade future option symbol based on input parameters.

    Args:
        symbol (str): Ticker symbol for the underlying future.
        future_month (str): Month code for the underlying future.
        option_product_code (str): Product code for the option.
        expiration_date (str): Expiration date of the option in yyyy-mm-dd format.
        option_type (str): Type of option, either "call" or "put".
        strike_price (float): Strike price of the option.

    Returns:
        str: Tastytrade future option symbol in the format "./FUTURE_MONTH OPTION_PRODUCT_CODE YYMMDDC/P STRIKE_PRICE".

    Example:
        >>> to_tastytrade_future_option_symbol("CL", "Z", "LO1X2", "2022-11-04", "call", 91.0)
        "./CLZ2 LO1X2 221104C91"
    """

    # Convert expiration date to yyMMdd format
    expiration_date_formatted = expiration_date[2:].replace('-', '')

    # Convert option type to C or P
    option_type_formatted = option_type[0].upper()

    # Convert strike price to 8-digit integer (multiply by 1000 and convert to int)
    strike_price_int = int(strike_price * 1000)

    # Combine all parts to form Tastytrade future option symbol
    future_option_symbol = f"./{symbol}{future_month} {option_product_code} {expiration_date_formatted}{option_type_formatted}{strike_price_int:05d}"

    return future_option_symbol

