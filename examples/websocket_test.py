import configparser
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


def main():
    from tastytrade_api.streamer.streamer import TastytradeStreamer
    from tastytrade_api.authentication import TastytradeAuth

    # Load configuration from file
    config = configparser.ConfigParser()
    config.read("config.ini")
    websocket_url = config["WEBSOCKET"]["websocket_url"]
    username = config.get('ACCOUNT', 'username')
    password = config.get('ACCOUNT', 'password')
    # Initialize the authentication object
    auth = TastytradeAuth(username, password)

    # Log in to the API
    auth_data = auth.login()
    session_token = auth.session_token

    streamer = TastytradeStreamer(session_token, websocket_url)
    streamer.connect()

    if streamer.wait_for_connection():
        streamer.start_heartbeat()
        streamer.public_watchlists_subscribe()
        streamer.quote_alerts_subscribe()
        while streamer.ws.sock and streamer.ws.sock.connected:
            time.sleep(1)


if __name__ == "__main__":
    main()
