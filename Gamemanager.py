import random
import time
import logging
import asyncio
import threading
import numpy as np

from sio_server import Server
from sio_client import Network as Client
from threading import Thread, Event

class Gamemanager:
    
    def __init__(self) -> None:
        pass

    def coin_flip(self) -> None:
        result = random.randint(0,2**16)
        connection.send_data("COIN", result)
        
    def determine_starting_player(self,opponent_coin):
        if self.coin > opponent_coin:
            return True 
        elif self.coin < opponent_coin:
            return False
        else:
            self.coin_flip()
                 
    def update_board(self, new_board: list) -> None:

        self.board = new_board
        self.won = self.game_over()
        if self.won == 1:
            print("gewinner einblenden")
        else:
            self.player = (self.player + 1) % 2
            self.turn()
            
    def checkboard(self, board_status, player):
        if player:
            player = "X"
        else:
            player = "O"
        answer = self.is_winner(board_status, player)
        answer2 = self.is_tie(board_status)
        if answer:
            return player
        elif answer2:
            return "Tie"
        
    def is_winner(self, board_status, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if board_status[i][0] == board_status[i][1] == board_status[i][2] == player:
                return True
            if board_status[0][i] == board_status[1][i] == board_status[2][i] == player:
                return True

        # Diagonals
        if board_status[0][0] == board_status[1][1] == board_status[2][2] == player:
            return True

        if board_status[0][2] == board_status[1][1] == board_status[2][0] == player:
            return True

        return False

    def is_tie(self, board_status):

        r, c = np.where(board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie
    
    def aimove(mode) -> list:
        if mode == "leicht":
            zug = print("move leicht ki")
            return zug
        if mode == "schwer":
            zug = print("move leicht ki")
            return zug

    def netzwerk_start():
        # Custom logging format to differentiate between threads
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)s) %(message)s')

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
    
    async def create_multiplayer_game(port):
        # Wait for the server to start
        await asyncio.sleep(5)

        # Create a client connection to the server
        connection = Client("localhost", port)
        
        # Add event listeners to execute when certain events are received
        connection.event_manager.add_listener(connection.CHAT_TYPE, lambda data: chat_receive(data, connection))
        connection.event_manager.add_listener(connection.ACK_TYPE, lambda data: print(data))

        # Discover available servers 
        connection.start_discover()
        while connection.DISCOVER_ON:
            await asyncio.sleep(1)
        print(connection.potential_servers)
    
    def chat_receive(data, connection):
        if data == connection.ACK_TYPE:
            print("ACK received")
        else:
            print(f"Chat received: {data}")
        
        # Sample routine to send an acknowledge message back to the server
        asyncio.create_task(connection.send_data(connection.ACK_TYPE, data))
    
    def leave():
        print("Spiel verlassen!")