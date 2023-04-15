import sys
import os

# add the parent directory of tastytrade_api to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    # Load configuration from file
    config = configparser.ConfigParser()
    config.read("config.ini")
    session_token = config["WEBSOCKET"]["session_token"]
    websocket_url = config["WEBSOCKET"]["websocket_url"]

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
