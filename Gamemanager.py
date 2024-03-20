import random
import time
import logging
import asyncio
import threading
import numpy as np

from gamestate.board import Board
from sio_server import Server
from sio_client import Network as Client
from threading import Thread, Event



class Gamemanager:
    
    def __init__(self) -> None:
        self.thread_shutdown = threading.Event()
        self.board = Board()
        self.connection = None
        self.coin = None
        self.move = None
        self.gegenermove = None

    def coin_flip(self):
        result = random.randint(0,2**16)
        self.connection.send_data(self.connection.COIN_TYPE, result)
        while self.coin == None:
            pass
        return self.coin
        
    def determine_starting_player(self,opponent_coin):
        if self.coin > opponent_coin:
            self.coin = True
            self.move = 1
        elif self.coin < opponent_coin:
            self.coin = False 
            self.move = 0
        else:
            result = random.randint(0,2**16)
            self.connection.send_data(self.connection.COIN_TYPE, result)
                 
    def update_board(self, i, j, player) -> None:
        if self.move == 1:
            self.board[i,j] = player
            data ={"var1": i,"var2": j,"var3": player}
            self.connection.send_data(self.connection.MOVE_TYPE,data)
            self.move = 0
        while self.move == 0:
            pass
        return self.gegenermove[1],self.gegenermove[2]
    
    def opponent_move(self, move):
        self.board[move["var1"],move["var2"]] = move["var3"]
        self.gegenermove = move
        self.move = 1
            
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

    def create_lobby(self, game_name):

        # Custom logging format to differentiate between threads
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)s) %(message)s')
        
        # If multiplayer is triggered, start the server and client threads
        # A session name and valid port should be provided
        if True:
            server_thread = threading.Thread(name="ServerThread", target=lambda: self.start_multiplayer_server(game_name, 50000))
            client_thread = threading.Thread(name="GameThread",target=lambda: asyncio.run(self.create_multiplayer_game(50000)))
            threads = [server_thread, client_thread]
            for thread in threads:
                thread.start()
        
            # Keep the main thread alive until a keyboard interrupt is detected
            #try:
            #    while not self.thread_shutdown.is_set():
            #        time.sleep(1)
            #except KeyboardInterrupt:
            #    logging.info("Stopping Threads . . .")
            #    self.thread_shutdown.set()
            #for thread in threads:
            #    thread.join()
                
    def start_multiplayer_server(self, name, port):
        server_instance = Server(session_name=name, session_port=port)
        asyncio.run(server_instance.start_server())
    
    async def create_multiplayer_game(self, port):
        # Wait for the server to start
        self.connection = Client("localhost", 50000)
        await asyncio.sleep(5)
        
        # Add event listeners to execute when certain events are received
        self.connection.event_manager.add_listener(self.connection.CHAT_TYPE, lambda data: self.chat_safe(data))
        self.connection.event_manager.add_listener(self.connection.COIN_TYPE, lambda data: self.determine_starting_player(data))
        self.connection.event_manager.add_listener(self.connection.MOVE_TYPE, lambda data: self.opponent_move(data))
       
        # Discover available servers 
        self.connection.start_discover()
        #while self.connection.DISCOVER_ON:
        #    await asyncio.sleep(1)
            
    def get_lobbys(self):
        return self.connection.potential_servers 
    
    async def connect(self, name, port):
        self.connection = Client(name, port)
        #logging.debug(self.connection)
    
    def send(self,msg):
        logging.debug(self.connection)
        self.connection.send_data(self.connection.CHAT_TYPE, msg)        
    
    def chat_safe(self, data):
        self.msg = data
        
    def receive(self):
        return self.msg

    def leave():
        print("Spiel verlassen!")