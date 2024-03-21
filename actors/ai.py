class Player():
    def __init__(self, board):
        self.board = board

    def player_move(self):
        """
        Get the player's move (row and column) from the user input.

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.

        Returns:
        - tuple: The selected row and column coordinates.

        This function uses a while loop to repeatedly prompt the player for input
        until a valid move is entered. It ensures that the input consists of valid
        integers within the range 0-2 and that the chosen cell on the board is empty.
        If the input is invalid, an appropriate error message is displayed.

        Example:
        If the player enters '1' for the row and '2' for the column,
        and the corresponding cell on the board is empty, the function returns (1, 2).
        """
        while True:
            try:
                # Get input for row and column from the player
                row = int(input("Enter row (0, 1, 2): "))
                col = int(input("Enter column (0, 1, 2): "))

                # Check if the input is within the valid range and the selected cell is empty
                if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row, col] == ' ':
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                # Handle the case where the input is not a valid integer
                print("Invalid input. Enter numbers between 0 and 2.")


class AI():
    def __init__(self, board, max_depth):
        self._board = board
        self._max_depth = max_depth

    def minimax(self, depth, is_maximizing):
        """
        Implement the Minimax algorithm for Tic-Tac-Toe.

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.
        - depth (int): The current depth in the recursive search of the game tree
        - is_maximizing (bool): Indicates whether the current player is maximizing (True) or minimizing (False).
        - max_depth (int): The maximum depth to explore in the game tree.

        Returns:
        - int: The calculated score for the current state of the board.

        This function recursively explores the game tree using the Minimax algorithm to determine the optimal move
        for the current player. It assigns scores to game states based on the outcome of the game or the specified depth.
        """

        # Base case: Check if the game is won by 'X' or 'O' or if it's a draw
        if self._board.check_win('X'):
            return -1                 # 'X' wins, return a negative value
        elif self._board.check_win('O'):
            return 1                  # 'O' wins, return a positive value
        elif self._board.is_draw() or depth == self._max_depth:
            return 0                  # It's a draw or reached the specified depth, return 0

        if is_maximizing:
            # If maximizing, initialize the maximum evaluation score to negative infinity
            max_eval = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self._board[i, j] == ' ':
                        # Simulate the move for the maximizing player ('O')
                        self._board[i, j] = 'O'
                        # Recursively call minimax for the next level with the minimizing player's turn
                        eval = self.minimax(depth + 1, False)
                        # Undo the move
                        self._board[i, j] = ' '
                        # Update the maximum evaluation score
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            # If minimizing, initialize the minimum evaluation score to positive infinity
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if self._board[i, j] == ' ':
                        # Simulate the move for the minimizing player ('X')
                        self._board[i, j] = 'X'
                        # Recursively call minimax for the next level with the maximizing player's turn
                        eval = self.minimax(depth + 1, True)
                        # Undo the move
                        self._board[i, j] = ' '
                        # Update the minimum evaluation score
                        min_eval = min(min_eval, eval)
            return min_eval


    def ai_move(self):
        """
        Determine the optimal move for the AI player using Minimax algorithm.

        Parameters:
        - board (list): A 2D list representing the Tic-Tac-Toe board.
        - max_depth (int): The maximum depth to explore in the Minimax algorithm

        Returns:
        - tuple: The coordinates (row, column) of the optimal move for the AI player.

        This function iterates through each empty space on the board, simulates placing an 'O' in that space,
        and evaluates the move using the Minimax algorithm. The AI player chooses the move with the highest
        evaluation score.
        """
        best_eval = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self._board[i, j] == ' ':
                    self._board[i, j] = 'O'
                    eval = self.minimax(0, False)
                    self._board[i, j] = ' '
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (i, j)

        return best_move



