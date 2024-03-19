"""
This file is used to showcase the usage of the current SocketIO implementation.

The code should and will be implemented by game_manager itself.
"""

import time
import logging
import asyncio
import threading

from sio_server import Server
from sio_client import Network as Client

thread_shutdown = threading.Event()


def main():
    # Custom logging format to differentiate between threads
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)s) %(message)s')

    # If multiplayer is triggered, start the server and client threads
    # A session name and valid port should be provided
    if True:
        server_thread = threading.Thread(name="ServerThread", target=lambda: start_multiplayer_server("MyGame", 50000))
        client_thread = threading.Thread(name="GameThread",target=lambda: asyncio.run(create_multiplayer_game(50000)))
        threads = [server_thread, client_thread]
        for thread in threads:
            thread.start()
    
        # Keep the main thread alive until a keyboard interrupt is detected
        try:
            while not thread_shutdown.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping Threads . . .")
            thread_shutdown.set()
        for thread in threads:
            thread.join()


def start_multiplayer_server(name, port):
    server_instance = Server(session_name=name, session_port=port)
    asyncio.run(server_instance.start_server())
    # pass


async def create_multiplayer_game(port):
    # Wait for the server to start
    await asyncio.sleep(5)

    # Create a client connection to the server
    connection = Client(port)
    
    # Add event listeners to execute when certain events are received
    connection.event_manager.add_listener(connection.CHAT_TYPE, lambda data: chat_receive(data, connection))
    connection.event_manager.add_listener(connection.ACK_TYPE, lambda data: print(data))

    # Discover available servers 
    potential_servers = await connection.discover()
    print(potential_servers)

    # Check if the server is available
    if await connection.connect():
        try:
            while not thread_shutdown.is_set():
                await test_chat(connection)

        except asyncio.CancelledError:
            logging.info("Game creation coroutine cancelled.")


async def test_chat(connection):
    await connection.send_data(connection.CHAT_TYPE, "This is a chat message")
    await asyncio.sleep(5)


# Sample event handler for chat messages
def chat_receive(data, connection):
    if data == connection.ACK_TYPE:
        print("ACK received")
    else:
        print(f"Chat received: {data}")
    
    # Sample routine to send an acknowledge message back to the server
    asyncio.create_task(connection.send_data(connection.ACK_TYPE, data))





if __name__ == "__main__":
    main()