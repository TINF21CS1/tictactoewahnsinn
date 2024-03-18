from tkinter import *
from tkinter import ttk
import json

# Global Settings
board_size = 600

class M_Window():
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
        self.singleplayer_canvas = Canvas(self.window, width=50, height=7, bg='lightgray')
        self.singleplayer_canvas.grid(row=1, column=1, sticky=N)

        # Singleplayer-Label in Singleplayer
        Label(self.singleplayer_canvas, text="Singleplayer (KI): ", bg='lightgray', width=15, height=2).grid(row=0, column=0, sticky=N, padx=5, pady=5)

        # Schwierigkeitsgrad für KI
        self.difficulty = ["leicht", "schwer"]
        self.Combo = ttk.Combobox(self.singleplayer_canvas, values = self.difficulty, state="readonly")
        self.Combo.set(" Schwierigkeitsgrad ")
        self.Combo.grid(row=0, column=0, sticky=N, padx=15, pady=45)

        # Create-Objekt
        self.create = Button(self.singleplayer_canvas, text="Create", command=self.singleplayer, width=10, height=3, bg='lightgray')
        self.create.grid(row=0, column=2, sticky=E, padx=20, pady=20)

        # Settings-Objekt
        self.settings_canvas = Button(self.window, text="Settings", command=self.settings, width=20, height=3, bg='lightgray')
        self.settings_canvas.grid(row=0, column=2, sticky=N+E, padx=20, pady=20)

        # Multiplayer-Objekt
        self.multiplayer_canvas = Button(self.window, text="Multiplayer", command=self.multiplayer, width=45, height=7, bg='lightgray')
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

        self.stats()

    def mainloop(self):
        self.window.mainloop()

    def initialize_stats(self, message):
        # Zeichne eine Nachricht im Stats-Objekt
        self.stats_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_version(self, message):
        # Zeichne eine Nachricht im Version-Objekt
        self.version_canvas.create_text(50, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    # Functions for stats
    
    def stats(self):
        # Stats-Box
        self.stats_frame = Frame(self.stats_canvas, bg='powderblue')
        self.stats_frame.pack(side='top', fill="both", padx=3, pady=40)

        self.stats_list = Listbox(self.stats_frame, font=('arial 10 bold italic'), height=5, width=40)
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

    def settings(self):
        pass

    def singleplayer(self):
        pass

    def multiplayer(self):
        pass

game_instance = Window()
game_instance.mainloop()
