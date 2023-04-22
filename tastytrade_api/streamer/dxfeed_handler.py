import websocket
import threading
import json
import time
from dx_mapping import Quote

class DxFeedClient:
    HEARTBEAT_INTERVAL_SECONDS = 10
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.ws = None
        self.client_id = None
        self.last_heartbeat_sent = time.time()
        self.handshake_complete = threading.Event()
    
    def send_heartbeat(self):
        while True:
            time.sleep(self.HEARTBEAT_INTERVAL_SECONDS)
            heartbeat_message = {
                "channel": "/meta/connect",
                "clientId": self.client_id,
                "connectionType": "websocket"
            }
            self.ws.send(json.dumps([heartbeat_message]))
            
    def on_message(self, ws, message):
        msg = json.loads(message)
        # print(msg)
        #print("----------------")
        #print("Message received", msg)
        #print("----------------")
           
        if msg[0]["channel"] == "/meta/handshake":
            if msg[0]["successful"]:
                self.client_id = msg[0]["clientId"]
                self.handshake_complete.set()
            else:
                print("Handshake failed")
        elif msg[0]["channel"] == "/meta/subscribe":
            if msg[0]["successful"]:
                print(f"Successfully subscribed to {msg[0]['subscription']}")
            else:
                print("Subscription failed")
        #elif msg[0]["channel"] == "/data/Quote":
        #   print('!!!!!!!!!!! DATA QUOTE')
        elif msg[0]["channel"] == "/service/data":
            quotes = Quote.from_json(json.dumps(msg))
            for quote in quotes:
                print(str(quote))

        
    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")
        self.handshake()
        self.start_heartbeat()
    
    def start_heartbeat(self):
        t = threading.Thread(target=self.send_heartbeat)
        t.daemon = True
        t.start()

    def handshake(self):
        handshake_message = {
            "channel": "/meta/handshake",
            "version": "1.0",
            "minimumVersion": "1.0",
            "supportedConnectionTypes": ["websocket"],
            "ext": {
                "com.devexperts.auth.AuthToken":  self.auth_token}
        }
        self.ws.send(json.dumps([handshake_message]))

    def subscribe(self, event_type, symbol):
        subscription_message = {
            "channel": "/service/sub",
            "clientId": self.client_id,
            "data": {
                "reset": False,
                "add": {
                    event_type: [symbol]
                }
            }
        }
        self.ws.send(json.dumps([subscription_message]))
        

    def connect(self):
        headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'User-Agent': 'My Python App'
        }
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)
        websocket_thread = threading.Thread(target=self.ws.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()
        

"""
auth_token = 'xxx'
websocket_url = 'wss://tasty-live-web.dxfeed.com/live/cometd'

# websocket.enableTrace(True) # Enable trace for debugging purposes

client = DxFeedClient(websocket_url, auth_token)
client.connect()

# Wait for the connection to be established and the handshake to be completed
client.handshake_complete.wait()

client.subscribe("Quote", "AAPL")
client.subscribe("Quote", "TSLA")

# Start the heartbeat thread
#heartbeat_thread = threading.Thread(target=client.send_heartbeat)
#heartbeat_thread.daemon = True
#heartbeat_thread.start()

# Subscribe to Quotes for AAPL
# client.subscribe("Profile", "IBM")


# Keep the connection open and process messages
while True:
    time.sleep(1)

"""