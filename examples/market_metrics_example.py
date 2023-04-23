from tastytrade_api.authentication import TastytradeAuth
from tastytrade_api.market_data.market_metrics import MarketMetrics
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('ACCOUNT', 'username')
password = config.get('ACCOUNT', 'password')
api_url = 'https://api.tastytrade.com'  

# Initialize the authentication object
auth = TastytradeAuth(username, password)

# Log in to the API
auth_data = auth.login()

market_metrics = MarketMetrics(auth.session_token, api_url)

# ---- Get Market Metrics

symbols = ["AAPL", "FB", "BRK/B"]
try:
    metrics_data = market_metrics.get_metrics(symbols)
    # TODO: Handle the market metrics data as needed
    print('Metrics data:', json.dumps(metrics_data, indent=4))

except Exception as e:
    # TODO: Handle the exception as needed
    print(str(e))
    
# -------------------------------------------------------------------------------

# ----  Get dividend data
symbol = "AAPL"
try:
    dividend_data = market_metrics.get_dividend_data(symbol)
    print('Dividend data:', json.dumps(dividend_data, indent=4))
except Exception as e:
    print(str(e))
    
# -------------------------------------------------------------------------------
g
# ---- Get earnings data
symbol = "AAPL"
start_date = "2020-01-01"
try:
    earnings_data = market_metrics.get_earnings_data(symbol, start_date)
    print('Earnings data:', json.dumps(earnings_data, indent=4))
except Exception as e:
    print(str(e))