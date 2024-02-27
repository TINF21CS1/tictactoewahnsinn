from tkinter import *
import numpy as np

# Global Settings
board_size = 600

class Window():
    
    def __init__(self):

        self.window = Tk()
        self.window.title('Tic-Tac-Toe - Join/Create Multiplayer Game')

        # Bildschirmgröße
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.window.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        self.window.state('zoomed') # Start als volles Fenster

        # Open-Lobbys-Objekt
        self.games_canvas = Canvas(self.window, width=board_size, height=board_size, bg='lightgray')
        self.games_canvas.grid(row=0, column=0, sticky=N+W, padx=20, pady=20)

        # Leave-Objekt
        self.leave_canvas = Canvas(self.window, width=100, height=50, bg='lightgray')
        self.leave_canvas.grid(row=1, column=0, sticky=S+W, padx=20, pady=20)

        # Join-Game-Objekt
        self.join_game_canvas = Canvas(self.window, width=200, height=100, bg='lightgray')
        self.join_game_canvas.grid(row=0, column=1, sticky=N+E, padx=200, pady=100)

        # Create-Game-Objekt
        self.create_game_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.create_game_canvas.grid(row=0, column=1, sticky=N+E, padx=200, pady=300)

        # Zellen konfigurieren
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.window.update_idletasks()
        min_width = (
            self.games_canvas.winfo_reqwidth() +
            self.leave_canvas.winfo_reqwidth() +
            self.join_game_canvas.winfo_reqwidth() +
            self.create_game_canvas.winfo_reqwidth() +
            80  # 20 Pixel Platz auf beiden Seiten
        )
        min_height = max(
            self.games_canvas.winfo_reqheight() + 20,  # 10 Pixel Platz oben und unten
            self.leave_canvas.winfo_reqheight() + 20
        )
        self.window.minsize(min_width, min_height)

        # Rendern der Objekte:
        self.initialize_stats("Open Lobbys:")
        self.initialize_leave("Leave")
        self.initialize_join_game("Join Game")
        self.initialize_create_game("Create Game")

    def mainloop(self):
        self.window.mainloop()

    def initialize_leave(self, message):
        # Zeichne eine Nachricht im Chat-Objekt
        self.leave_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.games_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_join_game(self, message):
        # Zeichne eine Nachricht im Join-Game-Objekt
        self.join_game_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_create_game(self, message):
        # Zeichne eine Nachricht im Create-Game-Objekt
        self.create_game_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

game_instance = Window()
game_instance.mainloop()