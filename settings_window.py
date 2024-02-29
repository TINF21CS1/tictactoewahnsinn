from tkinter import *
import numpy as np

# Global Settings
board_size = 600

class Window():
    
    def __init__(self):

        self.window = Tk()
        self.window.title('Tic-Tac-Toe - Settings')

        # Bildschirmgröße
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.window.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        # self.window.state('zoomed') # Start als volles Fenster

        # Aktuelle-Settings-Objekt
        self.current_settings_canvas = Canvas(self.window)
        self.current_settings_canvas.grid(row=0, column=1, sticky=N, pady=20)

        # ID-Objekt
        self.id_canvas = Canvas(self.window, width=200, height=50)
        self.id_canvas.grid(row=1, column=0, sticky=N+W, padx=20)

        # Name-Objekt
        self.name_canvas = Canvas(self.window, width=200, height=50)
        self.name_canvas.grid(row=2, column=0, sticky=N+W, padx=20)

        # Hauptmenü-Objekt
        self.main_menu_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.main_menu_canvas.grid(row=4, column=0, sticky=S+W, padx=20, pady=20)

        # Save-Settings-Objekt
        self.save_settings_canvas = Canvas(self.window, width=200, height=50, bg='lightgray')
        self.save_settings_canvas.grid(row=4, column=2, sticky=S+E, padx=20, pady=20)

        # Zellen konfigurieren
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.window.update_idletasks()
        min_width = (
            self.current_settings_canvas.winfo_reqwidth() +
            self.id_canvas.winfo_reqwidth() +
            self.save_settings_canvas.winfo_reqwidth() +
            80  # 20 Pixel Platz auf beiden Seiten
        )
        min_height = (
            self.current_settings_canvas.winfo_reqheight() +
            self.id_canvas.winfo_reqheight() +
            self.name_canvas.winfo_reqheight() +
            self.main_menu_canvas.winfo_reqheight() +
            20  # 10 Pixel Platz oben und unten
        )
        self.window.minsize(min_width, min_height)

        # Rendern der Objekte:
        self.initialize_current_settings("Aktuelle Einstellungen:")
        self.initialize_id("ID: ")
        self.initialize_name("Name: ")
        self.initialize_main_menu("Hauptmenü")
        self.initialize_save_settings("Save Settings")

    def mainloop(self):
        self.window.mainloop()

    def initialize_current_settings(self, message):
        # Zeichne eine Nachricht im Aktuelle-Settings-Objekt
        self.current_settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_id(self, message):
        # Zeichne eine Nachricht im ID-Objekt
        self.id_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_name(self, message):
        # Zeichne eine Nachricht im Name-Objekt
        self.name_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_main_menu(self, message):
        # Zeichne eine Nachricht im Hauptmenü-Objekt
        self.main_menu_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_save_settings(self, message):
        # Zeichne eine Nachricht im Save-Settings-Objekt
        self.save_settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

game_instance = Window()
game_instance.mainloop()
