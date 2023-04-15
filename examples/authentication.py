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

"""
if auth_data:
    print("Successfully logged in!")
else:
    print("Failed to log in.")

# Validate the session
is_valid = auth.validate_session()

if is_valid:
    print("Session is valid.")
else:
    print("Session is invalid or expired.")

# Destroy the session (log out)
if auth.destroy_session():
    print("Successfully logged out.")
else:
    print("Failed to log out.")
"""
