#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import font 
from actors import user
from actors import ai
from gamestate import board
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

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
        
        model = user.User()
        view = self.frames[ProfileCreation]
        controller = ProfileController(model, view)
        view.set_controller(controller)

        self.show_frame(ProfileCreation)

                 

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
        easy = ttk.Button(self, text='Easy', command=lambda: [frame_switcher.show_frame(Game), frame_switcher.frames[Game].set_ai_difficulty(1)])
        hard = ttk.Button(self, text='Hard', command=lambda: [frame_switcher.show_frame(Game), frame_switcher.frames[Game].set_ai_difficulty(4)])
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
        self.profile = Profile(self)
        self.profile.pack(fill='both', expand=True)

        self.add(self.profile, text='Profile')
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
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.difficulty = 0
        self.frame_switcher = frame_switcher 
         # Add Board to Game page
        self.view = BoardView(self)
        self.view.grid(column=0, row=1)
        
        # MVC for Board
        self.model = board.Board() 
        self.opponent = ai.AI(self.model, self.difficulty)
        self.controller = BoardController(self.model, self.view, self.opponent)
        self.view.set_controller(self.controller)
         

        # Add Chat to Game page
        chat = Chat(self)
        chat.grid(column=1, row=1)

        # Add Label to Game page
        self.label = ttk.Label(self, text='Ready?')
        self.label.grid(column=0, row=0)

    def change_label(self, argument):
        self.label.config(text=argument)
    
    def set_ai_difficulty(self, difficulty):
        self.difficulty = difficulty
        if type(self.opponent == ai.AI):
            self.opponent.change_depth(difficulty) 
            print(difficulty)

    def rematch_leave(self):
        self.placeholder = ttk.Frame(self)
        self.placeholder.grid(column=0, row=2)
        self.leave = ttk.Button(master=self.placeholder, text="Leave", command=lambda: self.frame_switcher.show_frame(ChooseGamemode))
        self.rematch = ttk.Button(master=self.placeholder, text="Rematch", command=lambda: self.controller.new_game())
        self.leave.pack(side=tk.LEFT, expand=True)
        self.rematch.pack(side=tk.LEFT, expand=True)



class BoardView(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self._cells = {}
        self.create_grid()
        self.container = container
        
    def set_controller(self, controller):
        self.controller = controller

    def clear_board(self):
       for button in self._cells:
            button.config(state='normal', text="")

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
        if event.widget['state'] != tk.DISABLED:
            clicked_btn = event.widget
            (row, col) = self._cells[clicked_btn]
            if self.controller:
                self.controller.move((row, col))
                self.update_button(clicked_btn, 'X')

    def update_button(self, arg, symbol):
        if type(arg) == tk.Button:
            (row, col) = self._cells[arg]
            symbol = self.controller.get_value((row, col))
            arg.config(text=symbol, state='disabled')
        if type(arg) == tuple:
            for key, value in self._cells.items():
                if value == arg:
                    symbol = self.controller.get_value(arg)
                    key.config(text=symbol, state='disabled')


class BoardController():
    def __init__(self, model, view, opponent):
        self.model = model
        self.view = view
        self.opponent = opponent 
    
    def new_game(self):
        self.model.clear_board()
        self.view.clear_board()
        self.view.container.placeholder.grid_forget()
        self.view.container.change_label("Player X's turn")

    def move(self, pos):
            try:
                self.model[pos] = 'X'
                self.model.display_board()
                print(self.check_win('X') and self.check_draw())
                if self.check_win('X') == True:
                    self.deactivate_buttons()
                    self.view.container.change_label("Player X won!")
                    self.view.container.frame_switcher.profile.controller.update_statistics("win")
                    self.view.container.rematch_leave()
                elif self.check_draw():
                    self.deactivate_buttons()
                    self.view.container.change_label("Draw")
                    self.view.container.rematch_leave()
                else: 
                    self.view.container.change_label("Player Y's turn")
                    self.opponent_move()

            except ValueError as error:
                print('error')
                self.view.show_error(error)
    
    def opponent_move(self):
            try:
                self.view.container.change_label("Player X's turn")
                pos = self.opponent.move()
                self.model[pos] = 'O'
                self.model.display_board()
                self.view.update_button(pos, 'Y')
                if self.check_win('O'):
                    self.deactivate_buttons()
                    self.view.container.change_label("Player O won!")
                    self.view.container.rematch_leave()
                elif self.check_draw():
                    self.deactivate_buttons()
                    self.view.container.change_label("Draw")
                    self.view.container.rematch_leave()

            except ValueError as error:
                print('error')
                self.view.show_error(error)
    
    def deactivate_buttons(self):
        for button in self.view._cells:
            button.config(state='disabled')

    def get_value(self, pos):
        try:
            return self.model[pos]
        except ValueError as error:
            print('error')
            self.view.show_error(error)
    
    def check_win(self, player):
        try:
            return self.model.check_win(player)
        except ValueError as error:
            print('error')
            self.view.show_error(error)

    def check_draw(self):
        try:
            return self.model.is_draw()
        except ValueError as error:
            print('error')
            self.view.show_error(error)


class Profile(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.model = user.User()
        self.controller = ProfileController(self.model, self)
        self.display_data()
   
    def set_controller(self, controller):
        self.controller = controller
    
    def display_data(self):
        data = self.controller.get_data()
        name = data.pop('name')
        uid = data.pop('id')
        stats = data.keys()
        occurences = data.values()
        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        axes = figure.add_subplot()
        axes.bar(stats, occurences)
        axes.set_xlabel('Wins / Draws / Losses')
        axes.set_ylabel('Count')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)        

class Chat(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        txt = tk.Text(self , width=60)
        scrollbar = ttk.Scrollbar(txt)

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

class ProfileController():
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

    def update_statistics(self, status):
        try:
            self.model._update_statistics(status)
        
        except ValueError as error:
            print('error')
            self.view.show_error(error)
    
    def get_data(self):
        return self.model.get_data()

    def update_statistics(self, status):
        try:
            self.model._update_statistics(status)
        
        except ValueError as error:
            print('error')
            self.view.show_error(error)
               

if __name__ == "__main__":
    app = App()
    app.mainloop()


