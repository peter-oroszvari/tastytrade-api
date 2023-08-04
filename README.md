# Tastytrade API Python SDK

_The Tastytrade API, which my Python module relies on, is currently in beta._

A Python client for the Tastytrade API, providing convenient access to Tastytrade's REST API for trading, account management, and more.

## Installation

Install the package using pip:

```bash
pip install tastytrade-api
```

## Usage

### Login
Provide your Tastytrade username and password and authenticate with the API. This has to be done first
since the session token obtained will be used in subsequent API calls. Any authentication failure will raise
a ValidationError exception.

```python
from tastytrade_api import ValidationError
from tastytrade_api.authentication import TastytradeAuth

username = "your_username"
password = "your_password"

# Initialize the authentication object
auth = TastytradeAuth(username, password)

# Log in to the API
try:
    auth_data = auth.login()
except ValidationError as e:
    print(e)
```

### Logout
```python
# Destroy the session (log out)
try:
    auth.destroy_session()
except ValidationError as e:
    print(e)
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



