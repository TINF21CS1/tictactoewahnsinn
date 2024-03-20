import socket
import asyncio
import logging
import socketio
import threading

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

    BROADCAST_PORT = Server.BROADCAST_PORT    # Port for listening to server broadcasts
    SERVER_BROADCAST = Server.BROADCAST_MESSAGE # Broadcast message format
    CLIENT_DISCOVER_TIMEOUT = 20                # Timeout for server discovery
    CLIENT_DISCOVER_DELAY = 2                   # Delay between server discovery attempts
    IS_DISCOVERING = False                      # Flag to enable server discovery

    broadcast_servers = []  # List of servers found during discovery
    potential_servers = []  # List of servers that can be connected to


    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.shutdown_flag = threading.Event()
        self.sio = socketio.AsyncClient()
        self.event_manager = NetworkEventManager()
        self.loop = asyncio.get_running_loop()
        self.register_event_handlers()


    def start_discover(self):
        """Starts listening for server broadcasts."""
        self.DISCOVER_ON = True
        self.loop.create_task(self.discover_servers())


    async def discover_servers(self):
        """Listens for broadcast messages from servers on the local network."""
        def listen():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('', self.BROADCAST_PORT)) 
                for i in range(self.CLIENT_DISCOVER_TIMEOUT):
                    sock.settimeout(1.0)
                    try:
                        data, addr = sock.recvfrom(1024)
                        data = data.decode('utf-8')
                        if data[:18] == self.SERVER_BROADCAST and all(server["host"] != addr[0] for server in self.broadcast_servers):
                            self.broadcast_servers.append({"host": addr[0], "port": data[len(self.SERVER_BROADCAST) + 1:]})
                        logging.debug(f"[Net-Discover] Received broadcast from {addr}")
                    except socket.timeout:
                        logging.debug(f"[Net-Discover] Listening for broadcasts...")
                        continue
        self.listen_thread = threading.Thread(name="GameThread-1) (Broadcast", target=listen, daemon=True)
        self.listen_thread.start()
        self.listen_thread.join()    
        logging.debug("[Net-Discover] Server discovery stopped")
        logging.debug(f"[Net-Discover] Found {self.broadcast_servers}") 

        for server in self.broadcast_servers:
            if await self.connect(server["host"], server["port"]):
                await self.sio.emit(self.SERVER_DISCOVER, server["host"])
                await asyncio.sleep(self.CLIENT_DISCOVER_DELAY)
                await self.sio.disconnect()
            else:
                logging.error(f"Failed to connect to {server['host']}:{server['port']}")

        self.DISCOVER_ON = False


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
                        "session_host": data["session_host"],
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


    async def connect(self, server_host, server_port):
        """Attempts to connect to the server and returns the success status."""
        host = server_host if server_host else self.server_host
        port = server_port if server_port else self.server_port
        try:
            await self.sio.connect(f'http://{host}:{port}')
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

