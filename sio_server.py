import asyncio
import logging
import socketio
import uvicorn
import socket

class Server:
    """A simple server class that handles socket connections and relays messages."""

    NETWORK_INFO = "NET_INFO"           # Event type for network information (e.g. connect/disconnect messages)
    NETWORK_WARNING = "NET_WARNING"     # Event type for network warnings (e.g. exceeded connections)
    NETWORK_DISCOVER = "NET_DISCOVER"   # Event type for network discovery (client checking for available servers)

    NETWORK_PACKET = "RELAY"            # Event type for network packet relay (client sending data to other client)
    MAX_CLIENTS = 2                     # Maximum number of clients allowed to connect to the server
    MIN_PORT = 50000                    # Minimum port number for the server
    MAX_PORT = 50015                    # Maximum port number for the server


    def __init__(self, session_name: str, session_port: int):
        """Initialize the server with a session name and port."""
        self.sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
        self.app = socketio.ASGIApp(self.sio)    

        self.session_name = session_name
        self.session_port = session_port
        self.connected_clients = []

    
    def register_event_handlers(self):

        @self.sio.on('connect')
        async def connect(sid, environ):
            """Handle a new incomming SocketIO connection."""
            try:
                if len(self.connected_clients) < self.MAX_CLIENTS:
                    if self.connected_clients:
                        await self.sio.emit(self.NETWORK_INFO, f"[Server-Connect] User {sid} connected", to=self.connected_clients[0])
                    logging.debug(f"[Server-Connect] Successfully connected: {sid}")
                    self.connected_clients.append(sid)
                else:
                    await self.sio.emit(self.NETWORK_WARNING, f"[Server-Connect] Disconnected due to exceeded connections", to=sid)
                    await self.sio.disconnect(sid)

            except Exception as e:
                logging.error(f"Error handling connect: {e}")


        @self.sio.on('disconnect')
        async def disconnect(sid):
            """Handle a disconnecting SocketIO connection."""
            try:
                other_client = [client for client in self.connected_clients if client != sid]
                if other_client:
                    await self.sio.emit(self.NETWORK_INFO, f"[Server-Disconnect] User {sid} disconnected", to=other_client[0])
                logging.debug(f"[Server-Disconnect] Successfully disconnected: {sid}")
                self.connected_clients.remove(sid)

            except Exception as e:
                logging.error(f"Error handling disconnect: {e}")

        
        @self.sio.on(self.NETWORK_DISCOVER)
        async def discover(sid):
            """Handle a network discovery request by a client."""
            await asyncio.sleep(1)
            try:
                if len(self.connected_clients) < self.MAX_CLIENTS + 1:
                    await self.sio.emit(self.NETWORK_DISCOVER, {"connectable": True, "player_count": len(self.connected_clients), "session_name": self.session_name, "session_port": self.session_port}, to=sid)
                    logging.debug(f"[Server-Discover] Discovered by {sid} (success)")

                else:
                    await self.sio.emit(self.NETWORK_DISCOVER, {"connectable": False}, to=sid)
                    logging.debug(f"[Server-Discover] Discovered by {sid} (failure)")

            except Exception as e:
                logging.error(f"Error handling disvover: {e}")


        @self.sio.on(self.NETWORK_PACKET)
        async def relay(sid, data):
            """Handle the network packet relay to the other client."""
            try:
                if 'event_type' not in data or 'data' not in data:
                    await self.sio.emit(self.NETWORK_WARNING, f"[Server-Packet] Invalid data format", to=sid)
                    return
                
                logging.info(f"[Net-Packet] Received {data} (from {sid})")
                other_client = [client for client in self.connected_clients if client != sid]

                if other_client:
                    await self.sio.emit(data["event_type"], data["data"], to=other_client[0])
                else:
                    await self.sio.emit(self.NETWORK_WARNING, "[Server-Packet] No clients available to send", to=sid)

            except Exception as e:
                logging.error(f"Error handling packet relay: {e}")
                await self.sio.emit(self.NETWORK_WARNING, "[Server-Packet] Error processing your request", to=sid)


    async def start_server(self):
        """Start the server and listen for incoming connections."""
        logging.basicConfig(level=logging.INFO)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', self.session_port)) == 0:
                logging.error(f"[Server-Init] Port {self.session_port} is already in use")
                return

        if self.session_port < self.MIN_PORT or self.session_port > self.MAX_PORT:
            logging.error(f"[Server-Init] Port {self.session_port} is out of range")
            return
        
        self.register_event_handlers()

        config = uvicorn.Config(self.app, host="localhost", port=self.session_port, log_level="info")
        server = uvicorn.Server(config)

        await server.serve()




if __name__ == "__main__":
    server_instance = Server(session_name="MyServer", session_port=50000)
    asyncio.run(server_instance.start_server())