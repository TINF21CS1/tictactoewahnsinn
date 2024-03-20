#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import font 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        container = ttk.Frame(self) 
        container.pack(side='top', fill='both', expand = True)
        
        self.title('TicTacToe')
        self.geometry('800x600')
        self.resizable(False, False)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        
        self.frames = {}
        

        for F in (ProfileCreation, Notebook):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(Notebook)

    def show_frame(self, frame_index):
        frame = self.frames[frame_index]
        frame.tkraise()

class ChooseGamemode(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        multiplayer = ttk.Button(self, text="Multiplayer", command=lambda: controller.show_frame(Multiplayer))
        singleplayer = ttk.Button(self, text="Singleplayer", command=lambda: controller.show_frame(ChooseAiLevel))
        multiplayer.pack()
        singleplayer.pack()
              
class Multiplayer(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

class ChooseAiLevel(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        easy = ttk.Button(self, text='Easy', command=lambda: controller.show_frame(Game))
        hard = ttk.Button(self, text='Hard', command=lambda: controller.show_frame(Game))
        easy.pack()
        hard.pack()

class Notebook(ttk.Notebook):
    def __init__(self, container, controller):
        super().__init__(container)

        self.frames = {} 
               
        for F in (ChooseGamemode, Multiplayer, ChooseAiLevel, Game):
            frame = F(self, self)

            self.frames[F] = frame
        
        # Create profile page and add to notebook
        profile = ttk.Frame(self)
        profile.pack(fill='both', expand=True)

        self.add(profile, text='Profile')
        self.show_frame(ChooseGamemode)

    def show_frame(self, frame):
        frame = self.insert(0, self.frames[frame], text='Game')
        self.select(0)
        if self.index('end') >= 3:
            self.hide(1)



class Game(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(0, weight=2)
   
         # Add Board to Game page
        board = Board(self, 1)
        board.grid(column=0, row=1)

        # Add Chat to Game page
        chat = Chat(self)
        chat.grid(column=1, row=1)

        # Add Label to Game page
        label = ttk.Label(self, text='Player X')
        label.grid(column=0, row=0)
 
def callback():
    print("clicked") 

class Board(ttk.Frame):
    def __init__(self, container, board):
        super().__init__(container)
        self.board = board
        self._cells = {}
        self.create_grid()

    def create_grid(self):
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=self,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

class Profile(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

class Cell(ttk.Button):
    def __init__(self, container, command, x, y):
        super().__init__(container)
        self.x = x
        self.y = y

class Chat(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        txt = tk.Text(self , width=60)
        scrollbar = ttk.Scrollbar(txt)

def create_profile():
    print("button pressed") 

class ProfileCreation(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        username_label = ttk.Label(self, text="Username")
        username_label.pack()
        self.username = tk.StringVar()
        username_entry = ttk.Entry(self, textvariable=self.username)
        username_entry.pack()
        create_button = ttk.Button(self, text="Create Profile", command=create_profile)
        create_button.pack()



if __name__ == "__main__":
    app = App()
    app.mainloop()


