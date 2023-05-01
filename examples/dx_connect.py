import asyncio
from tastytrade_api.streamer.dxfeed_handler import CometdWebsocketClient
from tastytrade_api.streamer.dx_mapping import Quote
import logging
from tastytrade_api.authentication import TastytradeAuth
import configparser
import json


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
    symbols = ["/VXMV23:XCBF", "AAPL"]
    for symbol in symbols:
        await client.send_subscription_message(client.websocket, event_type, symbol)   
     
async def consume_data(queue):
    while True:
        data = await queue.get()
        if data is None:
            break
        try:
            print("This is the raw data: ", data)
            quotes = Quote.from_list(data)
            for quote in quotes:
                print("Data received in script:", quote)
        except ValueError:
            print("Invalid data list received")
        
async def main():
    websocket_url = 'wss://tasty-live-web.dxfeed.com/live/cometd'
    data_queue = asyncio.Queue()

    client = CometdWebsocketClient(websocket_url, dxfeedtoken, data_queue, on_handshake_success)
    
    connect_task = asyncio.create_task(client.connect())
    consume_data_task = asyncio.create_task(consume_data(data_queue))

    await asyncio.gather(connect_task, consume_data_task)

if __name__ == "__main__":
    asyncio.run(main(), debug = True)