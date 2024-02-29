from tkinter import *
import numpy as np

# Global Settings
board_size = 600

class Window():
    def __init__(self):

        self.window = Tk()
        self.window.title('Tic-Tac-Toe - Main Window')

        # Bildschirmgröße
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.window.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        # self.window.state('zoomed') # Start als volles Fenster

        # Stats-Objekt
        self.stats_canvas = Canvas(self.window, width=300, height=200, bg='lightgray')
        self.stats_canvas.grid(row=0, column=0, sticky=N+W, padx=20, pady=20)

        # Quit-Objekt
        self.quit_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.quit_canvas.grid(row=3, column=0, sticky=W+S, padx=20, pady=20)

        # Singleplayer-Objekt
        self.singleplayer_canvas = Canvas(self.window, width=400, height=75, bg='lightgray')
        self.singleplayer_canvas.grid(row=1, column=1, sticky=N)

        # Settings-Objekt
        self.settings_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.settings_canvas.grid(row=0, column=2, sticky=N+E, padx=20, pady=20)

        # Multiplayer-Objekt
        self.multiplayer_canvas = Canvas(self.window, width=400, height=75, bg='lightgray')
        self.multiplayer_canvas.grid(row=2, column=1, sticky=N)

        # Version-Objekt
        self.version_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.version_canvas.grid(row=3, column=2, sticky=E+S, padx=20, pady=20)

        # Zellen konfigurieren
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.window.update_idletasks()
        min_width = (
            self.stats_canvas.winfo_reqwidth() +
            self.singleplayer_canvas.winfo_reqwidth() +
            self.settings_canvas.winfo_reqwidth() +
            80  # 20 Pixel Platz auf beiden Seiten
        )
        min_height = (
            self.stats_canvas.winfo_reqheight() +  
            self.singleplayer_canvas.winfo_reqheight() + 
            self.multiplayer_canvas.winfo_reqheight() +
            self.quit_canvas.winfo_reqheight() +
            20 # 10 Pixel Platz oben und unten
        )
        self.window.minsize(min_width, min_height) 

        # Rendern der Objekte:
        self.initialize_settings("Settings")
        self.initialize_stats("Stats:")
        self.initialize_singleplayer("Singleplayer-Game")
        self.initialize_multiplayer("Multiplayer-Game")
        self.initialize_quit("Quit")
        self.initialize_version("Version: 0.1")

    def mainloop(self):
        self.window.mainloop()

    def initialize_settings(self, message):
        # Zeichne eine Nachricht im Settings-Objekt
        self.settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.stats_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_singleplayer(self, message):
        # Zeichne eine Nachricht im Singleplayer-Objekt
        self.singleplayer_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_multiplayer(self, message):
        # Zeichne eine Nachricht im Multiplayer-Objekt
        self.multiplayer_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_quit(self, message):
        # Zeichne eine Nachricht im Quit-Objekt
        self.quit_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

game_instance = Window()
game_instance.mainloop()
