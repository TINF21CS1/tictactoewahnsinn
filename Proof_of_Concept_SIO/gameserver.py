import asyncio
import logging
import socketio
import uvicorn

class Server:
    """A simple server class that handles socket connections and relays messages."""
    NETWORK_PACKET = "RELAY"
    NETWORK_WARNING = "NET_WARNING"
    NETWORK_INFO = "NET_INFO"

    def __init__(self):
        self.sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
        self.app = socketio.ASGIApp(self.sio)
        self.clients = []
    

    def register_event_handlers(self):
        
        @self.sio.on('connect')
        async def connect(sid, environ):
            if self.clients:
                await self.sio.emit(self.NETWORK_INFO, f"User {sid} connected", to=self.clients[0])
            logging.info(f"Successfully connected: {sid}")
            self.clients.append(sid)

            if len(self.clients) > 2:
                await self.sio.disconnect(sid)

        @self.sio.on('disconnect')
        async def disconnect(sid):
            other_client = [client for client in self.clients if client != sid]
            if other_client:
                await self.sio.emit(self.NETWORK_INFO, f"User {sid} disconnected", to=other_client[0])
            logging.info(f"Disconnected: {sid}")
            self.clients.remove(sid)

        @self.sio.on(self.NETWORK_PACKET)
        async def relay(sid, data):
            logging.info(f'Packet from {sid}: {data}')
            other_client = [client for client in self.clients if client != sid]

            if other_client:
                await self.sio.emit(data["event_type"], data["data"], to=other_client[0])
            else:
                await self.sio.emit(self.NETWORK_WARNING, "No clients available to send", to=sid)


async def main():
    logging.basicConfig(level=logging.INFO)
    server_instance = Server()
    server_instance.register_event_handlers()

    config = uvicorn.Config(server_instance.app, host="localhost", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()



if __name__ == "__main__":
    asyncio.run(main())