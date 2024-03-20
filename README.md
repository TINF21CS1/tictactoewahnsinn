## Network Communication Framework (Tim)

The networking module uses `asyncio` and `socketio` for WebSocket communication, ensuring efficient and non-blocking exchanges. It supports server discovery through UDP packets, provides event handling, and allows for the creation and management of game-specific communication packets. Additionally, it enables external use of event listeners and triggers, and includes `send_data` functions for interfacing with other components.

### Key Components
- **Server Discovery:** Utilizes broadcast messages for automatic detection of game servers within the local network.
- **Event Handling:** Implements a dynamic event manager, trigger and listener and supporting diverse data types and server communications.
- **Data Transmission:** Enables exchange of game-relevant information such as chat messages, game state, and turn details.
- **Asynchronous Communication:** Employs asynchronous programming models for responsive network interactions.

### Core Classes
- **Network:** Manages server discovery, connections, and data transmission.
- **NetworkEventManager:** Facilitates event listening and handling.
- **Server:** Coordinates socket connections and message relaying for the TicTacToe game.


### Dependencies
- asyncio
- aiohttp
- socketio
- socketio-python
- uvicorn

### Usage
The server and client classes should always run in the full game implementation to work as intended. For a general understanding, both the server and client can be initiated using the following Python code snippets:

**Server Instance Initialization:**
```python
# Create a server instance
server_instance = Server(session_name="MyServer", session_port=50000)

# Start the server
asyncio.run(server_instance.start_server())
```

**Client Instance Initialization:**
```python
# Create a client instance
client = Network(server_host='localhost', server_port=50000)
```
---

**Establishing a Connection**

To establish a connection and send data, follow these steps:
```python
# Attempt to connect to the server
if await client.connect('localhost', 50000):
    # Send a chat message once connected
    await client.send_data(connection.CHAT_TYPE, "This is a chat message")
```

**Creating an Event Listener**

You can listen for specific events using the event listener. For example, to handle chat messages:
```python
def chat_receive(data, connection):
    print(f"Received chat data: {data}")

client.event_manager.add_listener(connection.CHAT_TYPE, lambda data: chat_receive(data, connection))

```

**Discovering Servers**

To initiate the discovery process and find active servers:

```python
# Start server discovery
client.start_discover()

# Wait until discovery is finished
while client.DISCOVER_ON:
    await asyncio.sleep(1)

# Retrieve the list of discovered servers
# Example output: [{'player_count': 1, 'session_name': 'MyServer', 'session_host': '127.0.0.1', 'session_port': 50000}]
servers = client.potential_servers
```
---
