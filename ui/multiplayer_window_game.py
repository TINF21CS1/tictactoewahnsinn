from tkinter import *
import numpy as np
import json
import test_manager as gamemanager

# Global Settings
board_size = 600
symbol_size = 40
symbol_thickness = 30
symbol_X_color = '#FF0000'
symbol_O_color = '#0000FF'

class MP_Window(Toplevel):
    def __init__(self, player_X):
        super().__init__()
        self.attributes("-topmost", True)
        self.title('Tic-Tac-Toe - Multiplayer Game')

        # Check for Win, Lose & Tie
        self.gm = gamemanager.manager()

        # Bildschirmgröße
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        self.state('zoomed') # Start als volles Fenster

        # Statistik-Objekt
        self.stats_canvas = Canvas(self, width=board_size/2, height=board_size, bg='lightgray')
        self.stats_canvas.grid(row=0, column=0, sticky=N+W, padx=20, pady=20)

        # Stats-Box
        self.stats_frame = Frame(self.stats_canvas, bg='powderblue')
        self.stats_frame.pack(side='top', fill="both", padx=3, pady=40)

        self.stats_list = Listbox(self.stats_frame, font=('arial 10 bold italic'), height=27, width=50)
        self.stats_list.pack(side=TOP, fill=BOTH)

        # Leave-Objekt
        self.leave_canvas = Button(self, text="Leave", command=self.destroy, width=10, height=2, bg='lightgray')
        self.leave_canvas.grid(row=1, column=0, sticky=S+W, padx=20, pady=20)

        # Board-Objekt
        self.board_canvas = Canvas(self, width=board_size, height=board_size)
        self.board_canvas.grid(row=0, column=1, sticky=N, pady=20)

        # Chat-Objekt
        self.chat_canvas = Canvas(self, width=board_size/2, height=board_size, bg='lightgray')
        self.chat_canvas.grid(row=0, column=2, sticky=N+E, padx=20, pady=20)

        # Zug-Objekt
        self.zug_canvas = Canvas(self, width=300, height=50, bg='lightgray')
        self.zug_canvas.grid(row=1, column=1, sticky=S, pady=50)

        # Version-Objekt
        self.version_canvas = Canvas(self, width=200, height=50, bg='lightgray')
        self.version_canvas.grid(row=1, column=2, sticky=E+S, padx=20, pady=20)

        # Zellen konfigurieren
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.update_idletasks()
        self.minsize(900, 700)

        if player_X == "True": # Zur Festlegung, ob X oder O
            self.player_X = True
        elif player_X == "False":
            self.player_X = False

        # Rendern der Objekte:
        self.initialize_board()
        self.initialize_chat("Chat:")
        self.initialize_stats("Stats:")
        self.initialize_version("Version: 0.1")
        self.initialize_zug("Currently on the move: ")
        
        self.chat()
        self.stats()
        self.zug()

        self.board_canvas.bind('<Button-1>', self.click)

        # Starteinstellungen
        self.board_status = np.zeros(shape=(3, 3))

    #def mainloop(self):
    #    self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.board_canvas.create_line((i + 1) * board_size / 3, 0, (i + 1) * board_size / 3, board_size)

        for i in range(2):
            self.board_canvas.create_line(0, (i + 1) * board_size / 3, board_size, (i + 1) * board_size / 3)

    def initialize_chat(self, message):
        # Zeichne eine Nachricht im Chat-Objekt
        self.chat_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_zug(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.zug_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.stats_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(50, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    # Functions for chat

    def receive(self, msg):
        while True:
            try:
                #msg = network.recv.decode("utf8")
                self.msg_list.insert(END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self, window=NONE):
        msg = self.my_msg.get()
        if len(msg) != 0: # Prevent sending of zero-fields
            self.msg_list.insert(END, " me: " + msg + "\n")
            self.my_msg.set("")  # Clears input field

            #network.send(bytes(msg, "utf8"))

    def chat(self):
        self.messages_frame = Frame(self.chat_canvas, bg='powderblue')
        self.messages_frame.pack(side='top', fill="x", padx=3, pady=40)

        self.scrollbar = Scrollbar(self.messages_frame)  # To navigate through past messages
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        # Message-History
        self.msg_list = Listbox(self.messages_frame, font=('arial 10 bold italic'), height=22, width=50, yscrollcommand=self.scrollbar.set)
        self.msg_list.pack(side=LEFT, fill=BOTH)

        # Sending messages
        self.send_messages = LabelFrame(self.chat_canvas, text=" Send Messages ", bg='powderblue')
        self.send_messages.pack(side='top', fill="both", padx=3)

        self.my_msg = StringVar()
        self.entry_field = Entry(self.send_messages, font=('arial 8 italic'), textvariable=self.my_msg, width=25)
        self.entry_field.bind("<Return>", self.send) #For sending via ENTER
        self.entry_field.pack(side=LEFT, padx=20, pady=20)

        # Additional send-button
        self.send_button = Button(self.send_messages, text="Send", command=self.send, width=8)
        self.send_button.pack(side=RIGHT, padx=20, pady=20)

    # Function for Zug

    def zug(self):
        # Stats-Box
        self.zug_frame = Frame(self.zug_canvas, bg='powderblue')
        self.zug_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.zug_list = Listbox(self.zug_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.zug_list.pack(side=RIGHT, fill=BOTH)

        with open("own_stats_example.json","r") as f:
            
            data_own = json.load(f)

        with open("enemy_stats_example.json","r") as g:
            data_enemy = json.load(g)
        
        # Only for initialization
        if self.player_X:
            self.zug_list.insert(END, data_own["name"] + " (Me) ")
        else:
            self.zug_list.insert(END, data_enemy["name"] + " (Enemy) ")

    # Function for stats
    
    def stats(self):
        self.stats_list.delete(0,END) # For update-functionality

        with open("own_stats_example.json","r") as f:
            data = json.load(f)
        
        # Own stats
        if len(data) != 0: # Prevent rendering empty data
            self.stats_list.insert(END, " Own Statistics (" + data["name"] + "): \n")

            self.stats_list.insert(END, " - Wins: " + data["wins"] + "\n")
            self.stats_list.insert(END, " - Ties: " + data["draws"] + "\n")
            self.stats_list.insert(END, " - Losses: " + data["losses"] + "\n")
            self.stats_list.insert(END, "")
        else:
            self.stats_list.insert(END, " Error while loading local statistics")
            self.stats_list.insert(END, "")

        with open("enemy_stats_example.json","r") as f:
            data = json.load(f)

        # Enemy stats
        if len(data) != 0: # Prevent rendering empty data
            self.stats_list.insert(END, " Own Statistics (" + data["name"] + "): \n")

            self.stats_list.insert(END, " - Wins: " + data["wins"] + "\n")
            self.stats_list.insert(END, " - Ties: " + data["draws"] + "\n")
            self.stats_list.insert(END, " - Losses: " + data["losses"] + "\n")
            self.stats_list.insert(END, "")
        else:
            self.stats_list.insert(END, " Error while loading local statistics")
            self.stats_list.insert(END, "")

        self.after(500, self.stats) # Update every half second
        
    # Functions for board
        
    def draw_O(self, logical_position):
        logical_position = np.array(logical_position) # Zellwert auf dem Board
        grid_position = self.logical_to_grid(logical_position) # Pixelwert in der Zelle
        self.board_canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size, grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness, outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.logical_to_grid(logical_position) # Pixelwert in der Zelle
        self.board_canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size, grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness, fill=symbol_X_color)
        self.board_canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size, grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness, fill=symbol_X_color)

    def logical_to_grid(self, logical_position):
        logical_position = np.array(logical_position, int)
        return (board_size / 3) * logical_position + board_size / 6

    def grid_to_logical(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (board_size / 3), int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True
        
    def display_gameover(self, winner):

        with open("own_stats_example.json","r") as f:
            data = json.load(f)

        with open("enemy_stats_example.json","r") as g:
            data_enemy = json.load(g)

        if winner == "X":
            text = f'{data["name"]} wins (X)'
            color = symbol_X_color
        elif winner == "O":
            text = f'{data_enemy["name"]} wins (O)'
            color = symbol_O_color
        else:
            text = 'Tie'
            color = 'gray'

        self.board_canvas.delete("all")
        self.board_canvas.create_text(board_size / 2, board_size / 3, font="cmr 30 bold", fill=color, text=text)

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.grid_to_logical(grid_position)

        if self.player_X and not self.is_grid_occupied(logical_position):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                check = self.gm.checkboard(self.board_status, self.player_X) # Check for Win, Lose & Tie
                self.player_X = False # Stetigen Wechsel

                print("Player X: " + str(self.board_status))
                print("Sende Board an O...") # Senden: Board
        else:
            if not self.is_grid_occupied(logical_position):
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                check = self.gm.checkboard(self.board_status, self.player_X) # Check for Win, Lose & Tie
                self.player_X = True # Stetigen Wechsel

                print("Player O: " + str(self.board_status))
                print("Sende Board an X...") # Senden: Board

        # Check for Win, Lose & Tie
        if check == "X":
            self.display_gameover("X")
            self.gm.update_stats("X") #wird durch User-Klasse gehandelt
        elif check == "O":
            self.display_gameover("O")
            self.gm.update_stats("O") #wird durch User-Klasse gehandelt
        elif check == "Tie":
            self.display_gameover("Tie")
            self.gm.update_stats("Tie") #wird durch User-Klasse gehandelt

        # Zug
        with open("own_stats_example.json","r") as f:
            data_own = json.load(f)

        with open("enemy_stats_example.json","r") as g:
            data_enemy = json.load(g)
        
        if not (check == "X" or check == "O" or check == "Tie"):
            if self.player_X:
                self.zug_list.delete(0,END)  # Clears Listbox
                self.zug_list.insert(END, data_own["name"] + " (Ich) ")
            else:
                self.zug_list.delete(0,END)  # Clears Listbox
                self.zug_list.insert(END, data_enemy["name"] + " (Gegner) ")