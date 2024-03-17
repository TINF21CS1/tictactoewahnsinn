def check_win(board, player):
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
        if all(board[row, col] == player for col in range(3)):
            return True

    # Check columns
    for col in range(3):
        if all(board[row, col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i, i] == player for i in range(3)) or all(board[i, 2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
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
    return all(board[row, col] != ' ' for row in range(3) for col in range(3))

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
        if check_win(self._board, 'X'):
            return -1                 # 'X' wins, return a negative value
        elif check_win(self._board, 'O'):
            return 1                  # 'O' wins, return a positive value
        elif is_draw(self._board) or depth == self._max_depth:
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


def main():
    """
    Run the main game loop for a simple Tic-Tac-Toe game.

    The game loop alternates between player and AI turns, displaying the current state of the board after each move.
    The loop continues until there is a winner ('X' or 'O'), a draw, or the player chooses to exit the game.

    This function uses the display_board, player_move, ai_move, check_win, and is_draw functions to implement the game logic.

    Example:
    Calling main() starts and runs the Tic-Tac-Toe game until a winner is declared or the game ends in a draw.
    """

    board = Board()
    player = Player(board)
    ai = AI(board, 1)
    
    player_turn = True

    while True:
        board.display_board()

        if player_turn:
            print("\n")
            print("Your turn:")
            row, col = player.player_move()
            print("\n")
            board[row, col] = 'X'
        else:
            print("\n")
            input("Press Enter for the Ai player to go...")
            """
            Change the depth explored by the AI player by changing the number in
            parentheses in the next line of code. The default value is 0.
            """
            row, col = ai.ai_move()    # TODO: Adjust the depth explored here!
            print("\n")
            board[row, col] = 'O'

        if check_win(board, 'X'):
            board.display_board()
            print("You win!")
            break
        elif check_win(board, 'O'):
            board.display_board()
            print("AI wins!")
            break
        elif is_draw(board):
            board.display_board()
            print("It's a draw!")
            break

        player_turn = not player_turn

if __name__ == "__main__":
    main()
