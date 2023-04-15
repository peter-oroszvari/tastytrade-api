import json
import logging
import time
from websocket import WebSocketApp
import threading

import functools


logger = logging.getLogger(__name__)

class TastytradeStreamer:
    """A class to handle the streaming of data from the Tastytrade API using WebSockets."""

    def __init__(self, session_token, websocket_url, message_callback=None, error_callback=None, open_callback=None, close_callback=None):
        self.session_token = session_token
        self.websocket_url = websocket_url
        self.ws = None
        self.message_callback = message_callback or self.on_message
        self.error_callback = error_callback or self.on_error
        self.open_callback = open_callback or self.on_open
        self.close_callback = close_callback or self.on_close

    def on_message(self, ws, message):
        """Default callback function for handling received messages."""
        data = json.loads(message)
        logger.info("Received message: %s", data)

    def on_error(self, ws, error):
        """Default callback function for handling errors."""
        logger.error("Error: %s", error)

    def on_close(self, ws, *args):
        """Default callback function for handling WebSocket close events."""
        logger.info("WebSocket closed")

    def on_open(self, ws):
        """Default callback function for handling WebSocket open events."""
        logger.info("WebSocket opened")

    def connect(self):
        def send_wrapper(ws, message):
            print(f"Sent message: {message}")
            return WebSocketApp.send(self.ws, message)
        
        """Connects to the WebSocket and sets the provided callback functions."""
        self.ws = WebSocketApp(
            self.websocket_url,
            on_message=self.message_callback,
            on_error=self.error_callback,
            on_close=self.close_callback,
            on_open=self.open_callback,
        )
        self.ws.send = functools.partial(send_wrapper, self.ws)

        websocket_thread = threading.Thread(target=self.ws.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

    def send_heartbeat(self):
        """Sends a heartbeat message to the server."""
        heartbeat_message = json.dumps({"auth-token": self.session_token,"action": "heartbeat", "value": ""})
        self.ws.send(heartbeat_message)
        logger.info("Sent heartbeat message")

    def connect_account(self, account_numbers):
        """Sends a connect message to subscribe to account level updates.

        Args:
            account_numbers (list): A list of account numbers to subscribe to.
        """
        connect_message = json.dumps({"action": "connect", "value": account_numbers})
        self.ws.send(connect_message)
        logger.info("Sent connect message for accounts: %s", account_numbers)
        
    def account_subscribe(self, account_numbers):
        """Sends an account-subscribe message to subscribe to account level updates.
           This method may be deprecated in the future, consider using 'connect_account' instead.
        Args:
            account_numbers (list): A list of account numbers to subscribe to.
        """
        account_subscribe_message = json.dumps({"auth-token": self.session_token, "action": "account-subscribe", "value": account_numbers})
        self.ws.send(account_subscribe_message)
        logger.warning("Sent account-subscribe message for accounts: %s. This method may be deprecated in the future, consider using 'connect_account' instead.", account_numbers)

    def start_heartbeat(self, interval=30):
        """Starts sending heartbeat messages at the specified interval (in seconds).

        Args:
            interval (int): The interval between heartbeat messages in seconds.
        """
        if not self.ws:
            logger.error("WebSocket is not connected. Please call 'connect' before starting the heartbeat.")
            return

        def send_heartbeat_periodically():
            while self.ws.sock and self.ws.sock.connected:
                self.send_heartbeat()
                time.sleep(interval)

        heartbeat_thread = threading.Thread(target=send_heartbeat_periodically)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        logger.info("Started heartbeat with an interval of %d seconds", interval)

    def public_watchlists_subscribe(self):
        """Sends a message to subscribe to public watchlist updates."""
        subscribe_message = json.dumps({"auth-token": self.session_token, "action": "public-watchlists-subscribe", "value": ""})
        self.ws.send(subscribe_message)
        logger.info("Sent public-watchlists-subscribe message")

    def quote_alerts_subscribe(self):
        """Sends a message to subscribe to quote alert messages."""
        subscribe_message = json.dumps({"auth-token": self.session_token, "action": "quote-alerts-subscribe", "value": ""})
        self.ws.send(subscribe_message)
        logger.info("Sent quote-alerts-subscribe message")

    def user_message_subscribe(self, user_external_id):
        """Sends a message to subscribe to user-level messages.

        Args:
            user_external_id (str): The user's external-id returned in the POST /sessions response.
        """
        subscribe_message = json.dumps({"auth-token": self.session_token, "action": "user-message-subscribe", "value": user_external_id})
        self.ws.send(subscribe_message)
        logger.info("Sent user-message-subscribe message for user_external_id: %s", user_external_id)
    
    def wait_for_connection(self, timeout=10):
        start_time = time.time()
        while not (self.ws.sock and self.ws.sock.connected) and time.time() - start_time < timeout:
            time.sleep(0.1)

        if not (self.ws.sock and self.ws.sock.connected):
            logger.error("WebSocket connection timed out")
            return False

        logger.info("WebSocket is connected")
        return True
'''
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

streamer = TastytradeStreamer("xxxx", "wss://streamer.tastyworks.com")
streamer.connect()

if streamer.wait_for_connection():
    streamer.start_heartbeat()
    streamer.public_watchlists_subscribe()
    streamer.quote_alerts_subscribe()
    while streamer.ws.sock and streamer.ws.sock.connected:
        time.sleep(1)
'''
