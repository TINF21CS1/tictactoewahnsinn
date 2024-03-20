#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import font 
from actors import user
from actors import ai
from gamestate import board

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
        
        self.show_frame(ProfileCreation)

        model = user.User()
        view = self.frames[ProfileCreation]
        controller = Controller(model, view)
        view.set_controller(controller)
         

    def show_frame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()

class ChooseGamemode(ttk.Frame):
    def __init__(self, container, frame_switcher):
        super().__init__(container)
        multiplayer = ttk.Button(self, text="Multiplayer", command=lambda: frame_switcher.show_frame(Multiplayer))
        singleplayer = ttk.Button(self, text="Singleplayer", command=lambda: frame_switcher.show_frame(ChooseAiLevel))
        multiplayer.pack()
        singleplayer.pack()
              
class Multiplayer(ttk.Frame):
    def __init__(self, container, frame_switcher):
        super().__init__(container)

class ChooseAiLevel(ttk.Frame):
    def __init__(self, container, frame_switcher):
        super().__init__(container)
        easy = ttk.Button(self, text='Easy', command=lambda: frame_switcher.show_frame(Game))
        hard = ttk.Button(self, text='Hard', command=lambda: frame_switcher.show_frame(Game))
        easy.pack()
        hard.pack()

class Notebook(ttk.Notebook):
    def __init__(self, container, frame_switcher):
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
    def __init__(self, container, frame_switcher):
        super().__init__(container)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(0, weight=2)
   
         # Add Board to Game page
        board_view = BoardView(self)
        board_view.grid(column=0, row=1)
        
        # MVC for Board
        model = board.Board() 
        view = board_view
        controller = BoardController(model, view)
        view.set_controller(controller)
         

        # Add Chat to Game page
        chat = Chat(self)
        chat.grid(column=1, row=1)

        # Add Label to Game page
        label = ttk.Label(self, text='Player X')
        label.grid(column=0, row=0)


class BoardView(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self._cells = {}
        self.create_grid()
        
    def set_controller(self, controller):
        self.controller = controller

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
                button.bind('<ButtonPress-1>', self.pressed)

                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )



    def pressed(self, event):
        clicked_btn = event.widget
        (row, col) = self._cells[clicked_btn]
        if self.controller:
            self.controller.move((row, col))
            self.controller.ai_move()
            
        

class BoardController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.ai = ai.AI(model, 4)

    def move(self, pos):
        try:
            self.model[pos] = 'X'
            self.model.display_board()

        except ValueError as error:
            print('error')
            self.view.show_error(error)
    
    def ai_move(self):
        try:
            pos = self.ai.ai_move()
            print(pos)
            self.model[pos] = 'O'
            self.model.display_board()
        except ValueError as error:
            print('error')
            self.view.show_error(error)
  
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
    def __init__(self, container, frame_switcher):
        super().__init__(container)
        username_label = ttk.Label(self, text="Username")
        username_label.pack()
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack()
        save_button = ttk.Button(self, text="Create Profile", command=self.save_button_clicked)
        save_button.pack()
        self.frame_switcher = frame_switcher
        self.controller = None
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.pack()

    def set_controller(self, controller):
        self.controller = controller

    def save_button_clicked(self):
        if self.controller:
            self.controller.save(self.username_var.get())

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        self.username_entry['foreground'] = 'red'

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        self.username_entry['foreground'] = 'black'
        self.username_var.set('')

    def hide_message(self):
        self.message_label['text'] = ''

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, username):
        try:
            self.model.change_name(username)
            self.model.save()

            self.view.show_success(f'The username {username} is saved!')
            self.view.after(1000, lambda:self.view.frame_switcher.show_frame(Notebook))

        except ValueError as error:
            print('error')
            self.view.show_error(error)

if __name__ == "__main__":
    app = App()
    app.mainloop()


