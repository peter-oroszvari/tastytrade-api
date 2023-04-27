import asyncio
from tastytrade_api.streamer.dxfeed_handler import CometdWebsocketClient
import logging
from tastytrade_api.authentication import TastytradeAuth
import configparser


logger = logging.getLogger(__name__)

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(log_handler)

logging.getLogger("websockets").setLevel(logging.DEBUG)

config = configparser.ConfigParser()
config.read("config.ini")
username = config.get('ACCOUNT', 'username')
password = config.get('ACCOUNT', 'password')
TTClient = TastytradeAuth(username, password)
TTClient.login()
get_token = TTClient.get_dxfeed_token()
dxfeedtoken = get_token['data']['token']
logger.debug('DxFeed Token:', dxfeedtoken)

async def on_handshake_success(client):
    event_type = "Quote"
    symbol = "AAPL"
    await client.send_subscription_message(client.websocket, event_type, symbol)



async def main():
    websocket_url = 'wss://tasty-live-web.dxfeed.com/live/cometd'

    client = CometdWebsocketClient(websocket_url, dxfeedtoken, on_handshake_success)

    await client.connect()

    listen_task = asyncio.create_task(client.listen(client.websocket))
    await listen_task

if __name__ == "__main__":
    asyncio.run(main(), debug = True)