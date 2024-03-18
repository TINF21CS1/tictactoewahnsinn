from tkinter import *
import json

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
        self.current_settings_canvas.grid(row=0, column=1, sticky=N+E, pady=20)

        # ID-Objekt
        self.id_canvas = Canvas(self.window, width=200, height=50)
        self.id_canvas.grid(row=0, column=0, sticky=N+W, padx=50, pady=150)

        # Name-Objekt
        self.name_canvas = Canvas(self.window, width=200, height=50)
        self.name_canvas.grid(row=0, column=0, sticky=N+W, padx=50, pady=250)

        # Leave-Objekt
        self.leave_canvas = Button(self.window, text="Leave", command=self.window.quit, width=10, height=2, bg='lightgray')
        self.leave_canvas.grid(row=4, column=0, sticky=S+W, padx=20, pady=20)

        # Settings-Objekt
        self.settings_canvas = Canvas(self.window, width=board_size/2, height=board_size, bg='lightgray')
        self.settings_canvas.grid(rowspan=3, row=0, column=2, sticky=N+E, padx=20, pady=100)

        # Save-Settings-Objekt
        self.save_settings_canvas = Button(self.window, text="Save Settings", command=self.save_settings, width=13, height=2, bg='lightgray')
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
            self.leave_canvas.winfo_reqheight() +
            20  # 10 Pixel Platz oben und unten
        )
        self.window.minsize(min_width, min_height)

        # Rendern der Objekte:
        self.initialize_current_settings("Aktuelle Einstellungen:")
        self.initialize_id("ID: ")
        self.initialize_name("Name: ")
        self.initialize_settings("Einstellungen ändern:")

        self.settings()
        self.id()
        self.name()

    def mainloop(self):
        self.window.mainloop()

    def initialize_settings(self, message):
        # Zeichne eine Nachricht im Chat-Objekt
        self.settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_current_settings(self, message):
        # Zeichne eine Nachricht im Aktuelle-Settings-Objekt
        self.current_settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_id(self, message):
        # Zeichne eine Nachricht im ID-Objekt
        self.id_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_name(self, message):
        # Zeichne eine Nachricht im Name-Objekt
        self.name_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def id(self):
        # ID-Box
        self.id_frame = Frame(self.id_canvas, bg='powderblue')
        self.id_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.id_list = Listbox(self.id_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.id_list.pack(side=RIGHT, fill=BOTH)

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.id_list.insert(END, data["id"])

    def name(self):
        # Name-Box
        self.name_frame = Frame(self.name_canvas, bg='powderblue')
        self.name_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.name_list = Listbox(self.name_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.name_list.pack(side=RIGHT, fill=BOTH)

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.name_list.insert(END, data["name"])
    
    def settings(self):
        # Create a Text widget
        self.text_frame = Text(self.settings_canvas, width=60, height=27)
        self.text_frame.pack(side='top', fill='both', padx=3, pady=40)

        with open("settings.json","r") as f:
            data = json.load(f)
        
        # Settings
        if len(data) != 0: # Prevent rendering empty data
            self.text_frame.insert(END, data)
        else:
            self.text_frame.insert(END, " Fehler beim Laden der Einstellungen")
            self.text_frame.insert(END, "")

    def save_settings(self):
        content = self.text_frame.get(1.0, END)
        content = content.replace("\'", "\"") # For valid json
        with open("settings.json", "w") as file:
            file.write(content)

game_instance = Window()
game_instance.mainloop()