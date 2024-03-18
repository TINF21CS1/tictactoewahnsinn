import sys
import client
import asyncio

async def main():
    # Create a network connection to the server
    connection = client.Network('http://localhost:8000') 

    # Register all necessary event handlers for Multiplayer
    connection.event_manager.add_listener(connection.CHAT_TYPE, lambda data: chat_receive(data, connection))
    connection.event_manager.add_listener(connection.ACK_TYPE, lambda data: print(data))
    connection.event_manager.add_listener(connection.EXIT_TYPE, lambda data: exit(data, connection))

    # Initiate Connection and send data
    if await connection.connect():
        while True:
            await connection.send_data("CHAT", "IT WOORKS!!!")
            await asyncio.sleep(5)


# Sample event handler for chat messages
def chat_receive(data, connection):
    if data == connection.ACK_TYPE:
        print("ACK received")
    else:
        print(f"Chat received: {data}")
    
    asyncio.create_task(connection.send_data(connection.ACK_TYPE, data))


# Sample event handler for exit messages
def exit(data, connection):
    print(f"Verbindung beendet ({data})")
    asyncio.create_task(connection.disconnect())
    sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())