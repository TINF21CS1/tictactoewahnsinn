#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('TicTacToe')
        self.geometry('800x600')
        self.resizable(False, False)


class Game(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(0, weight=2)

def callback():
    print("clicked") 

class Board(ttk.Frame):
    def __init__(self, container, board):
        super().__init__(container)
        self.board = board
        self._cells = {}

    def create_grid(self):
        for i in range(3):
            self.rowconfigure(i, weight=1, minsize=50)
            self.columnconfigure(i, weight=1, minsize=75)

class Profile(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

class Cell(ttk.Button):
    def __init__(self, container, command, x, y):
        super().__init__(container)
        self.x = x
        self.y = y



if __name__ == "__main__":
    app = App()
    # Create Notebook 
    notebook = ttk.Notebook()
    notebook.pack(pady=10, fill='both')
   
    # Create game page and add to notebook
    game = Game(notebook)
    game.pack(fill='both', expand=True)  
    notebook.add(game, text='Game')
    
    # Create profile page and add to notebook
    profile = ttk.Frame(notebook)
    profile.pack(fill='both', expand=True)
    notebook.add(profile, text='Profile')

    # Add Board to Game page
    board = Board(game, 1)
    board.grid(column=0, row=1)

    app.mainloop()


