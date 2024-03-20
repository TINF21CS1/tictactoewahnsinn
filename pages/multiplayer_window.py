from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox
from .multiplayer_window_game import MP_Window
from .. import Gamemanager as gamemanager

# Global Settings
board_size = 600

class L_Window(Toplevel):
    
    def __init__(self):
        super().__init__()
        self.title('Tic-Tac-Toe - Join/Create Multiplayer Game')

        # Handle connections
        self.gm = gamemanager.Gamemanager()

        # Bildschirmgröße
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        self.state('zoomed') # Start als volles Fenster

        # Open-Lobbys-Objekt
        self.games_canvas = Canvas(self, width=board_size, height=board_size, bg='lightgray')
        self.games_canvas.grid(rowspan=4, row=0, column=0, sticky=N+W, padx=20, pady=20)

        # Lobbys-Box
        self.lobbys_frame = Frame(self.games_canvas, bg='powderblue')
        self.lobbys_frame.pack(side='top', fill="both", padx=3, pady=40)

        self.lobbys_list = Listbox(self.lobbys_frame, font=('arial 10 bold italic'), height=30, width=75)
        self.lobbys_list.pack(side=TOP, fill=BOTH)

        # Join-Game-Objekt
        self.join_game_canvas = Button(self, text="Join Game (IP)", command=self.join_game, width=25, height=6, bg='lightgray')
        self.join_game_canvas.grid(row=1, column=1, sticky=N+E, padx=150)

        # Create-Game-Objekt
        self.create_game_canvas = Button(self, text="Create Game", command=self.create_game, width=25, height=3, bg='lightgray')
        self.create_game_canvas.grid(row=2, column=1, sticky=N+E, padx=150)

        # Leave-Objekt
        self.leave_canvas = Button(self, text="Leave", command=self.destroy, width=10, height=2, bg='lightgray')
        self.leave_canvas.grid(row=5, column=0, sticky=S+W, padx=20, pady=20)

        # Version-Objekt
        self.version_canvas = Canvas(self, width=200, height=50, bg='lightgray')
        self.version_canvas.grid(row=5, column=2, sticky=E+S, padx=20, pady=20)

        # Zellen konfigurieren
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.update_idletasks()
        self.minsize(900, 700)

        # Rendern der Objekte:
        self.initialize_stats("Open Lobbys:")
        self.initialize_version("Version: 0.1")

        self.lobbys()

    #def mainloop(self):
    #    self.window.mainloop()

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.games_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(50, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    # Function for finding lobby
    
    def lobbys(self):

        try:
            data = self.gm.get_lobbys()

            if len(data) != 0: # Prevent rendering empty data
                self.lobbys_list.insert(END, " Offene Lobbys: \n")

                self.lobbys_list.insert(END, " - " + data + "\n")
                self.lobbys_list.insert(END, "")
        except:
            self.lobbys_list.insert(END, " Keine offenen Lobbys vohanden ")
            self.lobbys_list.insert(END, "")

        self.after(500, self.lobbys) # Update every half second

    # Joining a multiplayer-game via description

    def join_game(self):
        ip = askstring("Connect to Multiplayer Game", "Enter Session_Name:Port:")
        if ip:
            print(ip)

            self.gm.connect(ip)

            #Connect to IP
            extra_window = MP_Window("False") # Client hat immer O

    # Host game

    def create_game(self):
        try:
            self.gm.create_lobby()
            extra_window = MP_Window("True") # Host hat immer X
        except:
            messagebox.showerror('Create Multiplayer Error', 'Fehler: Es konnte keine Lobby erstellt werden')