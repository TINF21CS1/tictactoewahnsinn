from actors.user import User
from actors.user import Opponent
from gamestate.board import Board
from actors.ai import Player
from actors.ai import AI

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
    ai = AI(board, 5)
    
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

        if board.check_win('X'):
            board.display_board()
            print("You win!")
            break
        elif board.check_win('O'):
            board.display_board()
            print("AI wins!")
            break
        elif board.is_draw():
            board.display_board()
            print("It's a draw!")
            break

        player_turn = not player_turn


main()
