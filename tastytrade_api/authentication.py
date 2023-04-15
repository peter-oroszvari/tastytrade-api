import requests
import time
from typing import Dict, Optional

class TastytradeAuth:
    def __init__(self, username: str, password: str = None, remember_token: str = None):
        self.username = username
        self.password = password
        self.remember_token = remember_token
        self.url = "https://api.tastytrade.com/sessions"
        self.session_token = None
        self.user_data = None
        self.token_timestamp = None

    def login(self, two_factor_code: str = None) -> Optional[Dict[str, str]]:
        payload = {
            "login": self.username,
            "remember-me": "true"
        }

        if self.password:
            payload["password"] = self.password
        elif self.remember_token:
            payload["remember-token"] = self.remember_token
        else:
            print("Error: Either password or remember token must be provided")
            return None

        headers = {}
        if two_factor_code:
            headers["X-Tastyworks-OTP"] = two_factor_code

        response = requests.post(self.url, headers=headers, data=payload)

        if response.status_code == 201:
            data = response.json()
            self.session_token = data['data']['session-token']
            self.remember_token = data['data']['remember-token']
            self.user_data = data['data']['user']
            self.token_timestamp = time.time()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None


    def validate_session(self) -> Optional[Dict[str, str]]:
        """
        Validates the current session using the session token.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the user data if the session is valid. Returns None if the session is invalid or there's an error.
        """
        url = "https://api.tastytrade.com/sessions/validate"
        headers = {"Authorization": self.session_token}

        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print("Response text:", response.text)

            return None

    def destroy_session(self) -> bool:
        """
        Destroys the current session, logging the user out.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        url = "https://api.tastytrade.com/sessions"
        headers = {"Authorization": self.session_token}

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            self.session_token = None
            self.remember_token = None
            self.user_data = None
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
