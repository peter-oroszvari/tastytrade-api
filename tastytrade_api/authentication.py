import requests
import time
from typing import Dict, Optional
from .exceptions import ValidationError

class TastytradeAuth:
    def __init__(self, username: str, password: str = None, remember_token: str = None):
        self.username = username
        self.password = password
        self.remember_token = remember_token
        self.url = "https://api.tastyworks.com"
        self.session_token = None
        self.user_data = None
        self.token_timestamp = None

    def _raise_validation_error(self, response):
        raise ValidationError(
            f"\nurl: {self.url}\n" \
            f"session_token: {self.session_token}\n" \
            f"user_data: {self.user_data}\n" \
            f"status_code: {response.status_code}\n" \
            f"reason: {response.reason}\n" \
            f"text: {response.text}")

    def login(self, two_factor_code: str = None) -> Dict[str, str]:
        """
        Creates a new user session with the Tastytrade API, using the username and password stored in the class.

        Args:
            two_factor_code (str): Specifies the two-factor authentication code, if the account has enabled it.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the user's session token and other related data.

        Raises:
            ValidationError: if the session is invalid or there's an error.
        """
        payload = {"login": self.username, "remember-me": "true"}

        if self.password:
            payload["password"] = self.password
        elif self.remember_token:
            payload["remember-token"] = self.remember_token
        else:
            raise ValidationError("Either password or remember token must be provided")

        headers = {}
        if two_factor_code:
            headers["X-Tastyworks-OTP"] = two_factor_code

        response = requests.post(f"{self.url}/sessions", headers=headers, data=payload)

        if response.status_code == 201:
            data = response.json()
            self.session_token = data["data"]["session-token"]
            self.remember_token = data["data"]["remember-token"]
            self.user_data = data["data"]["user"]
            self.token_timestamp = time.time()
            return data
        else:
            self._raise_validation_error(response)

    def validate_session(self) -> Dict[str, str]:
        """
        Validates the current session using the session token.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the user data if the session is valid.

        Raises:
            ValidationError: if the session is invalid or there's an error.
        """
        headers = {"Authorization": self.session_token}
        response = requests.post(f"{self.url}/sessions/validate", headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            self._raise_validation_error(response)

    def destroy_session(self):
        """
        Destroys the current session, logging the user out.

        Raises:
            ValidationError: if the session is invalid or there's an error.
        """
        headers = {"Authorization": self.session_token}
        response = requests.delete(f"{self.url}/sessions", headers=headers)

        if response.status_code == 204:
            self.session_token = None
            self.remember_token = None
            self.user_data = None
        else:
            self._raise_validation_error(response)

    def get_dxfeed_token(self) -> Dict[str, str]:
        """
        Retrieves the dxfeed token by making a request to the Tastytrade endpoint.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the dxfeed token and other related data.
            Returns None if there's an error.

        Raises:
            ValidationError: if the session is invalid or there's an error.
        """
        self.validate_session()

        url = f"{self.url}/quote-streamer-tokens"
        headers = {"Authorization": self.session_token}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            self._raise_validation_error(response)

    def create_session(
        self,
        username: str,
        password: str,
        remember_me: bool = False,
        remember_token: str = None,
    ) -> Dict[str, str]:
        """
        Creates a new user session with the Tastytrade API, using the specified username and password.

        Args:
            username (str): The username or email of the user.
            password (str): The password for the user's account.
            remember_me (bool): Whether the session should be extended for longer than normal via remember token.
            Defaults to False.
            remember_token (str): The remember token. Allows skipping for 2 factor within its window.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the user's session token and other related data.
            Returns None if there's an error.

        Raises:
            ValidationError: if the session is invalid or there's an error.
        """
        payload = {
            "login": username,
            "password": password,
            "remember-me": remember_me,
            "remember-token": remember_token,
        }

        headers = {}
        response = requests.post(f"{self.url}/sessions", headers=headers, json=payload)

        if response.status_code == 201:
            data = response.json()
            self.session_token = data["data"]["session-token"]
            self.remember_token = data["data"]["remember-token"]
            self.user_data = data["data"]["user"]
            self.token_timestamp = time.time()
            return data
        else:
            self._raise_validation_error(response)
