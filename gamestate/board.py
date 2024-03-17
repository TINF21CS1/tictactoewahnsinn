class Board:
    def __init__(self):
        self.state = board = [[' ' for _ in range(3)] for _ in range(3)]
    
    def display_board(self):
        """
        Display the current state of the Tic-Tac-Toe board.

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.

        Each cell of the board is displayed, separated by '|' for columns,
        and rows are separated by a line of dashes ('-----').

        Example:
        If the board is [['X', 'O', ' '], [' ', 'X', 'O'], ['O', ' ', 'X']],
        the output will be:
        X|O|
        -----
         |X|O
        -----
        O| |X
        """
        for i, row in enumerate(self.state):
            # Display the cells of the current row, separated by '|'
            print('|'.join(row))

            # Display a line of dashes to separate rows, but not after the last row
            if i < len(self.state) - 1:
                print('-' * 5)
     
    def __getitem__(self, pos):
        row, column = pos
        return self.state[row][column]

    def __setitem__(self, pos, value):
        row, column = pos
        self.state[row][column] = value


