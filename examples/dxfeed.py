auth_token = 'xxx'
websocket_url = 'wss://tasty-live-web.dxfeed.com/live/cometd'

# ćwebsocket.enableTrace(True) # Enable trace for debugging purposes

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
