from tastytrade_api.account.balances_positions import TastytradeAccountPositions
from tastytrade_api.authentication import TastytradeAuth
from tastytrade_api.account.account_handler import TastytradeAccount

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('ACCOUNT', 'username')
password = config.get('ACCOUNT', 'password')


# Initialize the authentication object
auth = TastytradeAuth(username, password)

# Log in to the API
auth_data = auth.login()
print("Session token:", auth.session_token)

account = TastytradeAccount(auth.session_token, "https://api.tastytrade.com")
accounts = account.get_accounts()
print(accounts)
"""

api_url = "https://api.tastytrade.com"

position = TastytradeAccountPositions(session_token, api_url)

positions = position.get_positions(account_number)
print('Positions:', json.dumps(positions, indent=4))
pos_list = position.get_positions(account_number, symbol="PBR")
print('Positions list:', json.dumps(pos_list, indent=4))
balances = position.get_account_balances(account_number)
print('Balances:', json.dumps(balances, indent=4))
balance_snapshot = position.get_balance_snapshots(account_number, time_of_day="BOD",  snapshot_date= "2023-01-01")
print('Balance snapshot: ', json.dumps(balance_snapshot,indent = 4))
"""