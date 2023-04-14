# Tastytrade API

_The Tastytrade API, which my Python module relies on, is currently in beta and not yet publicly accessible. As a result, you may not be able to test the functionality of this module until the API becomes available for public use._

A Python client for the Tastytrade API, providing convenient access to Tastytrade's REST API for trading, account management, and more.

## Installation

Install the package using pip:

```bash
pip install tastytrade-api
```

## USAGE

Here's an example of how to use the Tastytrade API client:
```python
from tastytrade_api.authentication import TastytradeAuth

username = "your_username"
password = "your_password"

# Initialize the authentication object
auth = TastytradeAuth(username, password)

# Log in to the API
auth_data = auth.login()

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
```

## Development

To run tests, first install the required development packages:

```bash
pip install -r requirements-dev.txt
```

Then, execute the tests using unittest:

```bash
python -m unittest discover
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.



