import asyncio
import socketio
import logging

from gameserver import Server


class NetworkEventManager:
    """Handles network events by managing listeners and triggering events."""

    def __init__(self):
        self._listeners = {}
        logging.debug("[Net-Event] Event Manager initialized")

    def add_listener(self, event_type:str, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        logging.debug(f"[Net-Event] Listener added: {event_type} -> {callback}")

    async def trigger_event(self, event_type:str, data):
        if event_type in self._listeners:
            logging.debug(f"[Net-Event] Trigger {event_type}")
            for callback in self._listeners[event_type]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
        else:
            logging.warning(f"[Net-Event] No listeners for event: {event_type}")


class Network:
    """Manages network communication and event handling with a game server."""

    CHAT_TYPE = "CHAT"
    DATA_TYPE = "DATA"
    EXIT_TYPE = "EXIT"
    ACK_TYPE = "ACK"

    def __init__(self, url):
        self.sio = socketio.AsyncClient()
        self.url = url
        self.event_manager = NetworkEventManager()
        self.register_event_handlers()

    def register_event_handlers(self):
        """ Handles the events from the server """
        @self.sio.on(Server.NETWORK_WARNING)
        async def warning(data):
            logging.warning(f'[Net-Warning] {data}')

        @self.sio.on(Server.NETWORK_INFO)
        async def info(data):
            logging.info(f'[Net-Info] {data}')

        @self.sio.on('*')
        async def any_event(event, data):
            logging.info(f'[Net-Any] ({event}) {data}')
            await self.event_manager.trigger_event(event, data)


    async def send_data(self, event, data):
        """Sends a packet with a specific type and data to the server"""
        try:
            await self.sio.emit(Server.NETWORK_PACKET, {"event_type": event, "data": data})
        except Exception as e:
            logging.error(f'[Net-SendData] Fehler: {e}')


    async def connect(self):
        """Attempts to connect to the server and returns the success status."""
        try:
            await self.sio.connect(self.url)
            return True
        except Exception as e:
            logging.error(f'[Net-Connect] Fehler: {e}')
            return False        