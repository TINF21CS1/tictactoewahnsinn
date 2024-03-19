import asyncio
import logging
import socketio

from sio_server import Server


class Network:
    """Manages network communication and event handling with a game server."""

    CHAT_TYPE = "CHAT"      # Event type for chat messages (e.g. player messages)
    DATA_TYPE = "DATA"      # Event type for game data (e.g. board positions)
    TURN_TYPE = "TURN"      # Event type for turn data (e.g. player's turn)
    ACK_TYPE = "ACK"        # Event type for acknowledge messages (e.g. successful move)

    SERVER_INFO = Server.NETWORK_INFO           # Event type for server information (e.g. connect/disconnect messages)
    SERVER_WARNING = Server.NETWORK_WARNING     # Event type for server warnings (e.g. exceeded connections)
    SERVER_PACKET = Server.NETWORK_PACKET       # Event type for server packet relay (client sending data to other client)
    SERVER_DISCOVER = Server.NETWORK_DISCOVER   # Event type for server discovery (client checking for available servers)
    SERVER_MIN_PORT = Server.MIN_PORT            # Minimum port number for the server
    SERVER_MAX_PORT = Server.MAX_PORT            # Maximum port number for the server

    potential_servers = []  # List of potential servers in the configured network


    def __init__(self, server_port):
        self.server_port = server_port
        self.sio = socketio.AsyncClient()
        self.event_manager = NetworkEventManager()
        self.register_event_handlers()


    def register_event_handlers(self):

        @self.sio.on(self.SERVER_INFO)
        async def info(data):
            """Handles server information messages."""
            logging.info(f'{data}')

        @self.sio.on(self.SERVER_WARNING)
        async def warning(data):
            """Handles server warning messages."""
            logging.warning(f'{data}')

        @self.sio.on(self.SERVER_DISCOVER)
        async def discover(data):
            """Handles server discovery messages."""
            logging.info(f"[Net-Discover] {data}")
            if data["connectable"] == True:
                try:
                    self.potential_servers.append({
                        "player_count": data["player_count"], 
                        "session_name": data["session_name"], 
                        "session_port": data["session_port"]
                    })
                    logging.info(f"[Net-Discover] Success on {data['session_port']}")
                except KeyError as e:
                    logging.error(f"[Net-Discover] Missing data {e}")
            else:
                logging.info(f"[Net-Discover] Failure on {data['session_port']}")

        @self.sio.on('*')
        async def any_event(event, data):
            """Handles any event and triggers the corresponding event."""
            logging.info(f"[Net-Any] ({event}): {data}")
            await self.event_manager.trigger_event(event, data)


    async def connect(self):
        """Attempts to connect to the server and returns the success status."""
        try:
            await self.sio.connect(f'http://localhost:{self.server_port}')
            return True
        except Exception as e:
            logging.error(f'[Net-Connect] Fehler: {e}')
            return False   


    async def send_data(self, event, data):
        """Sends a packet with a specific type and data to the server"""
        try:
            await self.sio.emit(self.SERVER_PACKET, {"event_type": event, "data": data})
        except Exception as e:
            logging.error(f'[Net-SendData] Fehler: {e}')

    
    async def discover(self):
        """Discovers potential servers in the local network."""
        try:
            self.potential_servers = []
            for port in range(self.SERVER_MIN_PORT, self.SERVER_MAX_PORT + 1):
                try:
                    await self.sio.connect(f'http://localhost:{port}')
                    await self.sio.emit(self.SERVER_DISCOVER)
                    await asyncio.sleep(4)
                    await self.sio.disconnect()

                except socketio.exceptions.ConnectionError:
                    logging.debug(f"[Net-Discover] No Service with port: {port}")
                    continue

                except Exception as e:
                    logging.error(f'[Net-Discover] Fehler: {e}')
                    continue
            
            return self.potential_servers
        
        except Exception as e:
            logging.error(f'[Net-Discover] Fehler: {e}')        



class NetworkEventManager:
    """Handles network events by managing listeners and triggering events."""

    def __init__(self):
        self._listeners = {}
        logging.debug("[Net-Event] Event Manager initialized")

    def add_listener(self, event_type:str, callback):
        """Adds a listener to a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        logging.debug(f"[Net-Event] Listener added: {event_type} -> {callback}")

    async def trigger_event(self, event_type:str, data):
        """Triggers an event and calls all listeners for the event type."""
        if event_type in self._listeners:
            logging.debug(f"[Net-Event] Trigger {event_type}")
            for callback in self._listeners[event_type]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
        else:
            logging.warning(f"[Net-Event] No listeners for event: {event_type}")

