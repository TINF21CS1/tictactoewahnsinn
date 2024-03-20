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

    def check_win(self, player):
        """
        Check if the specified player has won the Tic-Tac-Toe game.

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.
        - player (str): The player to check for a win ('X' or 'O').

        Returns:
        - bool: True if the specified player has won, False otherwise.

        This function checks for a win by the specified player in three directions: rows, columns, and diagonals.
        If a winning combination is found, the function returns True; otherwise, it returns False.

        Example:
        Calling check_win(board, 'X') returns True if 'X' has won the game.
        """
        # Check rows
        for row in range(3):
            if all(self[row, col] == player for col in range(3)):
                return True

        # Check columns
        for col in range(3):
            if all(self[row, col] == player for row in range(3)):
                return True

        # Check diagonals
        if all(self[i, i] == player for i in range(3)) or all(self[i, 2 - i] == player for i in range(3)):
            return True

        return False

    def is_draw(self):
        """
        Check if the Tic-Tac-Toe game is a draw (no more empty spaces on the board).

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.

        Returns:
        - bool: True if the game is a draw, False otherwise.

        This function checks if there are no more empty spaces (' ') on the board, indicating a draw.

        Example:
        Calling is_draw(board) returns True if the game is a draw.
        """
        # Check if the game is a draw (no more empty spaces on the board)
        return all(self[row, col] != ' ' for row in range(3) for col in range(3))
