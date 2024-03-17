from tkinter import *
import numpy as np
import json

# Global Settings
board_size = 600
symbol_size = 40
symbol_thickness = 30
symbol_X_color = '#FF0000'
symbol_O_color = '#0000FF'

class Window():
    def __init__(self):

        self.window = Tk()
        self.window.title('Tic-Tac-Toe - Multiplayer Game')

        # Bildschirmgröße
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.window.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        # self.window.state('zoomed') # Start als volles Fenster

        # Statistik-Objekt
        self.stats_canvas = Canvas(self.window, width=board_size/2, height=board_size, bg='lightgray')
        self.stats_canvas.grid(row=0, column=0, sticky=N+W, padx=20, pady=20)

        # Leave-Objekt
        self.leave_canvas = Button(self.window, text="Leave", command=self.window.quit, width=10, height=2, bg='lightgray')
        self.leave_canvas.grid(row=1, column=0, sticky=S+W, padx=20, pady=20)

        # Board-Objekt
        self.board_canvas = Canvas(self.window, width=board_size, height=board_size)
        self.board_canvas.grid(row=0, column=1, sticky=N, pady=20)

        # Chat-Objekt
        self.chat_canvas = Canvas(self.window, width=board_size/2, height=board_size, bg='lightgray')
        self.chat_canvas.grid(row=0, column=2, sticky=N+E, padx=20, pady=20)

        # Version-Objekt
        self.version_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.version_canvas.grid(row=1, column=2, sticky=E+S, padx=20, pady=20)

        # Zellen konfigurieren
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.window.update_idletasks()
        min_width = self.stats_canvas.winfo_reqwidth() + self.board_canvas.winfo_reqwidth() + self.chat_canvas.winfo_reqwidth() + 40  # 20 Pixel Platz auf beiden Seiten
        min_height = self.stats_canvas.winfo_reqheight() + self.leave_canvas.winfo_reqheight() + 20  # 10 Pixel Platz oben und unten
        self.window.minsize(min_width, min_height)

        # Rendern der Objekte:
        self.initialize_board()
        self.initialize_chat("Chat:")
        self.initialize_stats("Stats:")
        self.initialize_version("Version: 0.1")
        
        self.chat()
        self.stats()

        self.window.bind('<Button-1>', self.click)

        # Starteinstellungen
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_turns = False
        self.player_X_starts = False

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.board_canvas.create_line((i + 1) * board_size / 3, 0, (i + 1) * board_size / 3, board_size)

        for i in range(2):
            self.board_canvas.create_line(0, (i + 1) * board_size / 3, board_size, (i + 1) * board_size / 3)

    def initialize_chat(self, message):
        # Zeichne eine Nachricht im Chat-Objekt
        self.chat_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.stats_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    # Functions for chat

    def receive(self):
        while True:
            try:
                #msg = network.recv.decode("utf8") #TODO: Chat empfangen
                self.msg_list.insert(END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self, window=NONE):
        msg = self.my_msg.get()
        if len(msg) != 0: # Prevent sending of zero-fields
            msg = ' me: ' + msg + '\n'
            self.msg_list.insert(END, msg)
            self.my_msg.set("")  # Clears input field

            #network.send(bytes(msg, "utf8")) #TODO: Chat senden

    def chat(self):
        self.messages_frame = Frame(self.chat_canvas, bg='powderblue')
        self.messages_frame.pack(side='top', fill="x", padx=3, pady=40)

        self.scrollbar = Scrollbar(self.messages_frame)  # To navigate through past messages
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        # Message-History
        self.msg_list = Listbox(self.messages_frame, font=('arial 10 bold italic'), height=27, width=50, yscrollcommand=self.scrollbar.set)
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

    # Functions for stats
    
    def stats(self):
        # Stats-Box
        self.stats_frame = Frame(self.stats_canvas, bg='powderblue')
        self.stats_frame.pack(side='top', fill="both", padx=3, pady=40)

        self.stats_list = Listbox(self.stats_frame, font=('arial 10 bold italic'), height=27, width=50)
        self.stats_list.pack(side=TOP, fill=BOTH)

        with open("own_stats_example.json","r") as f:
            data = json.load(f)
        
        # Own stats
        if len(data) != 0: # Prevent rendering empty data
            self.stats_list.insert(END, " Eigene Statistiken (" + data["name"] + "): \n")

            self.stats_list.insert(END, " - Siege: " + data["wins"] + "\n")
            self.stats_list.insert(END, " - Unentschieden: " + data["draws"] + "\n")
            self.stats_list.insert(END, " - Niederlage: " + data["losses"] + "\n")
            self.stats_list.insert(END, "")
        else:
            self.stats_list.insert(END, " Fehler beim Laden der eigenen Statistiken")
            self.stats_list.insert(END, "")

        with open("enemy_stats_example.json","r") as f:
            data = json.load(f)
            
        # Enemy stats
        if len(data) != 0: # Prevent rendering empty data
            self.stats_list.insert(END, " Eigene Statistiken (" + data["name"] + "): \n")

            self.stats_list.insert(END, " - Siege: " + data["wins"] + "\n")
            self.stats_list.insert(END, " - Unentschieden: " + data["draws"] + "\n")
            self.stats_list.insert(END, " - Niederlage: " + data["losses"] + "\n")
            self.stats_list.insert(END, "")
        else:
            self.stats_list.insert(END, " Fehler beim Laden der gegnerischen Statistiken")
            self.stats_list.insert(END, "")
        
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

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.grid_to_logical(grid_position)

        if self.player_X_turns:
            if not self.is_grid_occupied(logical_position):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.player_X_turns = not self.player_X_turns
        else:
            if not self.is_grid_occupied(logical_position):
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                self.player_X_turns = not self.player_X_turns

game_instance = Window()
game_instance.mainloop()