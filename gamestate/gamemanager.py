import ki
import Multiplayer
import Player
import random
from threading import Thread, Event

class Gamemanager:
    
    def __init__(self) -> None:

        self.board = self.create_board()
        self.player = 0
        self.player_turn = None
        self.won = None
        self.multiplayer = None
        self.privategame = None
        self.ai_level = None
        self.shutdown_event = Event()
        
    def start_game(self, multiplayer: bool, privategame: bool, ai_level: int)  -> None:

        self.multiplayer = multiplayer
        self.privategame = privategame
        self.ai_level = ai_level
        self.board = self.create_board()

        if self.multiplayer:
            try:
                if self.privategame:
                    multiplayer_thread = Thread(target=Multiplayer.main)
                    multiplayer_thread.start()
                    server = Multiplayer.server
                else:
                    multiplayer_thread = Thread(target=Multiplayer.main)
                    multiplayer_thread.start()
                    server = Multiplayer.server
            except:
                print("Es konnte kein Multiplayer sitzung erstellt werden.")

        try:
            if not server:
                self.player = 1
                Multiplayer.receive()
            else:
                self.coin_flip()
        except:
            print("Es konnte kein Server festgestellt werden")
        

        try:
            while True:
                if self.shutdown_event.is_set():
                    break
        except KeyboardInterrupt:
            self.shutdown_event.set()

        multiplayer_thread.join()

    def create_board(self) -> list:

        board = [None] * 9
        return board
    
    def coin_flip(self) -> None:

        result = random.randint(0, 1)
        self.player_turn = result
        Multiplayer.send(result)
        self.turn()
      
    def turn(self) -> None:
        
        if self.ai_level > 0 and self.player_turn ==1:
            ki.spielzug(self.board)
        else:
            print("funktion aufrufen das die Spieler wissen das die dran sind")
            
        
        
    def update_board(self, new_board: list) -> None:

        self.board = new_board
        self.won = self.game_over()
        if self.won == 1:
            print("gewinner einblenden")
        else:
            self.player = (self.player + 1) % 2
            self.turn()
  

    def game_over(self) -> bool:

        # Check horizontally
        for i in range(0, 3, 7):  
            if self.board[i] is not None and self.board[i] == self.board[i + 1] == self.board[i + 2]:
                self.result = self.board[i]
                return True,self.result
        
        # Check vertically
        for i in range(3): 
            if self.board[i] is not None and self.board[i] == self.board[i + 3] == self.board[i + 6]:
                self.result = self.board[i]
                return True,self.result
        
        # Check for diagonal
        if self.board[i] is not None and ((self.board[0] == self.board[4] == self.board[8]) or (self.board[2] == self.board[4] == self.board[6])):  # Check diagonally
            self.result = self.board[4]
            return True,self.result
        
        # Check for a draw
        available = [i for i, val in enumerate(self.board) if val is None]
        if available[0] is None:
            self.result = "draw"
            return True,self.result
        else:
            return False

    def validate_move(self, spielzug: int, player: bool) -> None:

        if player == self.player_turn:
            count_diff = 0
            new_board = self.board
            new_board[spielzug] = player
            for i in range(len(self.board)):
                if self.board[i] != new_board[i]:
                    if self.board[i] == None:
                        count_diff += 1
                    else:
                        print("Fehler: Ein bereits vergebener Wert wurde überschrieben!")     
        else:
            print("Fehler: Spieler ist nicht am Zug!")
        
        if count_diff == 1:
            if self.ai_level == 0:    
                Multiplayer.send(spielzug)
            self.update_board(new_board)
        else:
            print("Fehler: Fehlerhafter Spielzug. Es wurden zu viele oder keine Werte geändert!")  
    
    def reconnect():
        print("Funktion Netzerk neustarten")
    
    def leave():
        print("Spiel verlassen!")