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
<<<<<<< Updated upstream
### The TicTacToe Game Manager is a Python class designed to facilitate the management of TicTacToe multiplayer modes. It provides functionalities for game setup, board management, player movements, win/tie conditions checking, lobby creation, server-client communication, and more.

### Dependencies
-asyncio
-aiohttp
-socketio
-You can install these dependencies using pip:

**Set up the game lobby:**
game_manager.create_lobbyt("MyGameLobby", 5000)

**Connect to the game lobby:**
game_manager.connect("MyGameLobby", 5000)

Interact with the game:
# Example: Send a chat message
game_manager.send("Hello, everyone!")

# Example: Make a move on the board
game_manager.update_board(0, 0, 1)  # Player 1 moves to position (0, 0)
Features

# Game Setup: Create and manage game lobbies for multiplayer games.
# Board Management: Update and check the status of the game board.
# Player Movements: Make moves on the board and handle opponent moves.
# Win/Tie Conditions: Check for win or tie conditions after each move.
# Server-Client Communication: Facilitate communication between game clients and servers.
# Multiplayer Support
# The TicTacToe Game Manager supports multiplayer mode through server-client architecture. It enables the creation of game lobbies, discovery of available servers, and communication between game clients.





=======

## UI (Chris)

The UI uses tkinter as main component and was designed to have a ground up structure (start from main menu up to multiplayer-game), where the windows inherit everything important from the parent-window. The clean design is quite similar in every window for easy, straightforward debugging and good user experience. Every window is structured using the grid-layout from tkinter, where every object is placed inside a object-canvas to have an easy option for repositioning.

### Key Components/Classes
- **Main-Window:** Start of the game with a clean and easy user experience with display of own statistics.
- **Lobby-Window:** Display open game-lobbys, join a lobby or create one.
- **Singleplayer-Window:** Play against an ai-opponent (two difficulty-modes) and display statistics.
- **Multiplayer-Window:** Play against an opponent over the network and display own and enemy statistics.
- **Settings-Window:** Change and inspect own settings like id, name, country.

### Dependencies
- numpy

### Usage
All classes should always run in the full game implementation to work as intended. For testing purposes, every window can be tested separately using the mainloop()-function (removing the inheritance-part at the beginning of the class first)
>>>>>>> Stashed changes
