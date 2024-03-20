from tkinter import *
import json

# Global Settings
board_size = 600

class S_Window(Toplevel):
    
    def __init__(self):
        super().__init__()

        self.title('Tic-Tac-Toe - Settings')

        # Bildschirmgröße
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position für die Zentrierung des Fensters
        x_position = (screen_width - board_size) // 2
        y_position = (screen_height - board_size) // 2

        # Fenstergröße und Position
        self.geometry(f'{board_size}x{board_size}+{x_position}+{y_position}')
        self.state('zoomed') # Start als volles Fenster

        # Aktuelle-Settings-Objekt
        self.current_settings_canvas = Canvas(self)
        self.current_settings_canvas.grid(row=0, column=1, sticky=N+E, pady=20)

        # ID-Objekt
        self.id_canvas = Canvas(self, width=175, height=50)
        self.id_canvas.grid(row=0, column=0, sticky=S+W, padx=75, pady=100)

        # ID-Box
        self.id_frame = Frame(self.id_canvas, width=175, bg='powderblue')
        self.id_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.id_list = Listbox(self.id_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.id_list.pack(side=RIGHT, fill=BOTH)

        # Name-Objekt
        self.name_canvas = Canvas(self, width=175, height=50)
        self.name_canvas.grid(row=0, column=0, sticky=S+W, padx=75, pady=50)

        # Name-Box
        self.name_frame = Frame(self.name_canvas, width=175, bg='powderblue')
        self.name_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.name_list = Listbox(self.name_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.name_list.pack(side=RIGHT, fill=BOTH)

        # Straße-Objekt
        self.street_canvas = Canvas(self, width=175, height=50)
        self.street_canvas.grid(row=0, column=0, sticky=S+W, padx=75)

        # Street-Box
        self.street_frame = Frame(self.street_canvas, width=175, bg='powderblue')
        self.street_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.street_list = Listbox(self.street_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.street_list.pack(side=RIGHT, fill=BOTH)

        # PLZ-Objekt
        self.plz_canvas = Canvas(self, width=175, height=50)
        self.plz_canvas.grid(row=1, column=0, sticky=N+W, padx=75)

        # Plz-Box
        self.plz_frame = Frame(self.plz_canvas, width=175, bg='powderblue')
        self.plz_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.plz_list = Listbox(self.plz_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.plz_list.pack(side=RIGHT, fill=BOTH)

        # Land-Objekt
        self.country_canvas = Canvas(self, width=175, height=50)
        self.country_canvas.grid(row=1, column=0, sticky=N+W, padx=75, pady=50)

        # Country-Box
        self.country_frame = Frame(self.country_canvas, width=175, bg='powderblue')
        self.country_frame.pack(side='right', fill="both", padx=200, pady=20)

        self.country_list = Listbox(self.country_frame, font=('arial 10 bold italic'), height=1, width=25)
        self.country_list.pack(side=RIGHT, fill=BOTH)

        # Leave-Objekt
        self.leave_canvas = Button(self, text="Leave", command=self.destroy, width=10, height=2, bg='lightgray')
        self.leave_canvas.grid(row=4, column=0, sticky=S+W, padx=20, pady=20)

        # Settings-Objekt
        self.settings_canvas = Canvas(self, width=board_size/2, height=board_size, bg='lightgray')
        self.settings_canvas.grid(rowspan=3, row=0, column=2, sticky=N+E, padx=20, pady=100)

        # Save-Settings-Objekt
        self.save_settings_canvas = Button(self, text="Save Settings", command=self.save_settings, width=13, height=2, bg='lightgray')
        self.save_settings_canvas.grid(row=4, column=2, sticky=S+E, padx=20, pady=20)

        # Zellen konfigurieren
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Mindestgröße des Fensters festlegen
        self.update_idletasks()
        self.minsize(900, 700)

        # Rendern der Objekte:
        self.initialize_current_settings("Aktuelle Einstellungen:")
        self.initialize_id("ID: ")
        self.initialize_name("Name: ")
        self.initialize_street("Strasse: ")
        self.initialize_plz("PLZ: ")
        self.initialize_country("Land: ")
        self.initialize_settings("Einstellungen ändern:")

        self.settings()
        self.id()
        self.name()
        self.street()
        self.plz()
        self.country()

    #def mainloop(self):
    #   self.window.mainloop()

    def initialize_settings(self, message):
        # Zeichne eine Nachricht im Chat-Objekt
        self.settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_current_settings(self, message):
        # Zeichne eine Nachricht im Aktuelle-Settings-Objekt
        self.current_settings_canvas.create_text(10, 10, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_id(self, message):
        # Zeichne eine Nachricht im ID-Objekt
        self.id_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_name(self, message):
        # Zeichne eine Nachricht im Name-Objekt
        self.name_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_street(self, message):
        # Zeichne eine Nachricht im Street-Objekt
        self.street_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_plz(self, message):
        # Zeichne eine Nachricht im PLZ-Objekt
        self.plz_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    def initialize_country(self, message):
        # Zeichne eine Nachricht im Country-Objekt
        self.country_canvas.create_text(10, 20, anchor='nw', font="cmr 12", fill="black", text=message)

    # Generating the entries

    def id(self):
        self.id_list.delete(0,END) # For update-functionality

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.id_list.insert(END, data["id"])

    def name(self):
        self.name_list.delete(0,END) # For update-functionality

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.name_list.insert(END, data["name"])

    def street(self):
        self.street_list.delete(0,END) # For update-functionality

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.street_list.insert(END, data["street"])

    def plz(self):
        self.plz_list.delete(0,END) # For update-functionality

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.plz_list.insert(END, data["plz"])

    def country(self):
        self.country_list.delete(0,END) # For update-functionality

        with open("settings.json","r") as f:
            
            data = json.load(f)

        if data:
            self.country_list.insert(END, data["country"])

    # Changing the settings
    
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

    # Save the changed settings

    def save_settings(self):
        content = self.text_frame.get(1.0, END)
        content = content.replace("\'", "\"") # For valid json
        with open("settings.json", "w") as file:
            file.write(content)
        
        # Update all settings
        self.id()
        self.name()
        self.street()
        self.plz()
        self.country()