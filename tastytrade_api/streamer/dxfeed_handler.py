import asyncio
import json
import websockets
import logging

logger = logging.getLogger(__name__)

class CometdWebsocketClient:
    def __init__(self, url, auth_token, on_handshake_success=None):
        self.url = url
        self.auth_token = auth_token
        self.on_handshake_success = on_handshake_success
        self.message_id = 0
    
    def next_id(self):
        self.message_id += 1
        return str(self.message_id)

    async def connect(self):
        headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'User-Agent': 'My Python App'
        }

        async with websockets.connect(self.url, extra_headers=headers) as websocket:
            self.websocket = websocket
            handshake = asyncio.create_task(self.send_handshake(websocket))
            heartbeat = asyncio.create_task(self.send_heartbeat(websocket))
            listen = asyncio.create_task(self.listen(websocket))
            await asyncio.gather(handshake, heartbeat, listen)

    async def send_handshake(self, websocket):
        handshake_message = {
            "id": self.next_id(),
            "version": "1.0",
            "minimumVersion": "1.0",
            "channel": "/meta/handshake",
            "supportedConnectionTypes": ["websocket","long-polling","callback-polling"],
            "ext": {
                "com.devexperts.auth.AuthToken":  self.auth_token
            },
            "advice": {
                "timeout":60000,
                "interval":0
            }
        }
        handshake_str = json.dumps([handshake_message])
        await websocket.send(handshake_str)

    async def send_subscription_message(self, websocket, event_type, symbol):
        subscription_message = {
            "id": self.next_id(),
            "channel": "/service/sub",
            "clientId": self.client_id,
            "data": {
                "reset": True,
                "add": {
                    event_type: [symbol]
                }
            }
        }
        subscription_str = json.dumps([subscription_message])
        await websocket.send(subscription_str)

    async def listen(self, websocket):
        while True:
            message = await websocket.recv()
            await self.handle_message(message)
        
    async def handle_message(self, message):
        data = json.loads(message)
        logger.debug(f"Received message: {data}")

        if data and isinstance(data, list) and "channel" in data[0]:
            channel = data[0]["channel"]

            if channel == "/meta/handshake":
                await self.process_handshake(data[0])

            elif channel == "/service/sub":
                if data[0].get("successful", False):
                    logger.debug("Subscription successful")
                    await self.send_connect_message(self.websocket)
                else:
                    logger.warning("Subscription failed")
            
            elif channel == "/data":
                if data[0].get("data"):
                    logger.info(f"Data message received: {data[0]['data']}")
                else:
                    logger.warning("Data message has no data field")

        else:
            logger.warning(f"Unexpected message format: {message}")


    async def process_handshake(self, handshake_data):
        if "successful" in handshake_data and handshake_data["successful"] and "clientId" in handshake_data:
            self.client_id = handshake_data["clientId"]
            logger.debug(f"Handshake successful, client ID: {self.client_id}")

                    # Call the on_handshake_success callback if provided
            if self.on_handshake_success:
                await self.on_handshake_success(self)


    async def send_connect_message(self, websocket):
        connect_message = {
            "id": self.next_id(),
            "channel": "/meta/connect",
            "clientId": self.client_id,
            "connectionType": "websocket"
        }
        connect_str = json.dumps([connect_message])
        await websocket.send(connect_str)
        
    async def send_heartbeat(self, websocket):
        while True:
            await asyncio.sleep(10)  # Send the heartbeat every 10 seconds
            heartbeat_message = {
                 "id": self.next_id(),
                "channel": "/meta/connect",
                "clientId": self.client_id,
                "connectionType": "websocket"
            }
            await websocket.send(json.dumps([heartbeat_message]))