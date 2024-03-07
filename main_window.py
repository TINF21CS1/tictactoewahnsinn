from tkinter import *
from tkinter import ttk

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
        self.quit_canvas = Button(self.window, text="Quit", command=self.window.quit, width=10, height=2, bg='lightgray')
        self.quit_canvas.grid(row=3, column=0, sticky=S+W, padx=20, pady=20)

        # Singleplayer-Objekt
        self.singleplayer_canvas = Frame(self.window, width=50, height=7, bg='lightgray')
        self.singleplayer_canvas.grid(row=1, column=1, sticky=N)

        # Singleplayer-Label in Singleplayer
        Label(self.singleplayer_canvas, text="Singleplayer: ", bg='lightgray', width=20, height=3).grid(row=0, column=0, padx=5, pady=5)

        # Schwierigkeitsgrad für KI
        self.difficulty = ["leicht", "schwer"]
        self.Combo = ttk.Combobox(self.singleplayer_canvas, values = self.difficulty, state="readonly")
        self.Combo.set("Schwierigkeitsgrad")
        self.Combo.grid(padx = 5, pady = 5)

        # Create-Objekt
        self.create = Button(self.singleplayer_canvas, text="Create", command=self.singleplayer, width=10, height=3, bg='lightgray')
        self.create.grid(row=0, column=2, sticky=E, padx=20, pady=20)

        # Settings-Objekt
        self.settings_canvas = Button(self.window, text="Settings", command=self.settings, width=20, height=3, bg='lightgray')
        self.settings_canvas.grid(row=0, column=2, sticky=N+E, padx=20, pady=20)

        # Multiplayer-Objekt
        self.multiplayer_canvas = Button(self.window, text="Multiplayer", command=self.multiplayer, width=50, height=7, bg='lightgray')
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
        self.initialize_stats("Stats:")
        self.initialize_version("Version: 0.1")

    def mainloop(self):
        self.window.mainloop()

    def settings(self):
        pass

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.stats_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def singleplayer(self):
        pass

    def multiplayer(self):
        pass

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

game_instance = Window()
game_instance.mainloop()
