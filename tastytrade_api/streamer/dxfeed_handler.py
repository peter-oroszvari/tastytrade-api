import asyncio
import json
import websockets
import logging

logger = logging.getLogger(__name__)

class CometdWebsocketClient:
    def __init__(self, url, auth_token, data_queue, on_handshake_success=None):
        """
        Initialize a new instance of the class.

        :param url: The URL to connect to.
        :param auth_token: The authentication token to use.
        :param data_queue: The queue to put data into.
        :param on_handshake_success: Optional function to call on successful handshake.
         """
        self.url = url
        self.auth_token = auth_token
        self.on_handshake_success = on_handshake_success
        self.message_id = 0
        self.data_queue = data_queue
    
    def next_id(self):
        self.message_id += 1
        return str(self.message_id)

    async def connect(self):
        """
        Connect to the websocket server using the URL and authorization token provided
        during initialization. 
        """
        headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'User-Agent': 'My Python App'
        }
        """ ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        """
        # async with websockets.connect(self.url, extra_headers=headers, ssl=ssl_context) as websocket:
        async with websockets.connect(self.url, extra_headers=headers) as websocket:
            self.websocket = websocket
            await self.send_handshake(websocket)
            heartbeat = asyncio.create_task(self.send_heartbeat(websocket))

            # Process data messages from the listen method
            async for message_data in self.listen(websocket):
             #   print("Received data:", message_data)
                await self.data_queue.put(message_data)


            # Make sure the heartbeat task is canceled
            heartbeat.cancel()
            await asyncio.gather(heartbeat, return_exceptions=True)


    async def send_handshake(self, websocket):
        """
        Sends a handshake message to the specified WebSocket connection.

        Parameters:
        - websocket: the WebSocket connection to send the handshake to.

        Returns:
        - None

        Raises:
        - Any exceptions raised by the underlying websocket.send() call.

        The handshake message is a JSON-encoded dictionary with the following keys:
        - id: a unique identifier for the message
        - version: the version of the Bayeux protocol used
        - minimumVersion: the minimum version of the Bayeux protocol supported
        - channel: the channel to which the message is being sent
        - supportedConnectionTypes: a list of supported connection types
        - ext: an extension dictionary containing additional data
        - advice: an advice dictionary with the following keys:
            - timeout: the maximum time to wait for a response
            - interval: the minimum time between retries

        The handshake message is sent as a JSON-encoded array with a single element,
        containing the handshake message as its only element.
        """
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

    async def send_subscription_message(self, websocket, event_type, symbol, on_subscription_success=None):
        """
        Sends a subscription message to the specified websocket for the specified event type and symbol.
        :param websocket: The websocket to send the subscription message to.
        :param event_type: The event type to subscribe to.
        :param symbol: The symbol to subscribe to.
        :param on_subscription_success: Optional callback function to execute upon successful subscription.
        :return: None
        """
        subscription_message = {
            "id": self.next_id(),
            "channel": "/service/sub",
            "clientId": self.client_id,
            "data": {
                "reset": False, # If true, the subscription will be reset after each new message
                "add": {
                    event_type: [symbol]
                }
            }
        }
        subscription_str = json.dumps([subscription_message])
        await websocket.send(subscription_str)

    async def listen(self, websocket):
        """
        Continuously listens for messages from the given WebSocket and yields
        data messages as they arrive.

        :param websocket: The WebSocket to listen on.
        :type websocket: websockets.WebSocketCommonProtocol
        :yields: The data messages received from the WebSocket.
        :rtype: Any
        """
        while True:
            message = await websocket.recv()
            async for data_message in self.handle_message(message):
                yield data_message
           
        
    async def handle_message(self, message):
        """
        Handle incoming message data.

        Args:
            message (str): The incoming message data as a JSON string.

        Yields:
            The message data if it is a "/service/data" message.

        Raises:
            None.

        Returns:
            None.
        """
        data = json.loads(message)
        # logger.debug(f"Received message: {data}")

        if data and isinstance(data, list) and "channel" in data[0]:
            channel = data[0]["channel"]

            if channel == "/meta/handshake":
                await self.process_handshake(data[0])

            elif channel == "/service/sub":
                if data[0].get("successful", False):
                    logger.debug("Subscription successful")
                else:
                    logger.warning("Subscription failed")
            
            elif channel == "/service/data":
                if data[0].get("data"):
                    yield data[0]['data']
                else:
                    logger.warning("Data message has no data field")

        else:
            logger.warning(f"Unexpected message format: {message}")


    async def process_handshake(self, handshake_data):
        """
        Process the handshake data received from the server.

        If the handshake is successful and contains a client ID, update the client ID
        of this WebSocket client and log a debug message. If an on_handshake_success
        callback was provided, call it with this WebSocket client as argument.

        :param handshake_data: A dictionary containing the handshake data.
        :type handshake_data: dict
        """
        if "successful" in handshake_data and handshake_data["successful"] and "clientId" in handshake_data:
            self.client_id = handshake_data["clientId"]
            logger.debug(f"Handshake successful, client ID: {self.client_id}")

                    # Call the on_handshake_success callback if provided
            if self.on_handshake_success:
                await self.on_handshake_success(self)


    async def send_connect_message(self, websocket):
        """
        Sends a heartbeat message every 10 seconds to keep the WebSocket connection alive.

        :param websocket: the WebSocket object to send the message to
        :type websocket: WebSocket
        """
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