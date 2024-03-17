import random
import Gamemanager

class AI:
    def spielzug(board):
        # Find all empty positions on the board
        empty_positions = [i for i, val in enumerate(board) if val is None]
        
        # Check if there are any empty positions
        if empty_positions:
            # Choose a random empty position
            position_to_fill = random.choice(empty_positions)
            # Return the chosen postion
            Gamemanager.validate_move(position_to_fill, 1)
        else:
            # No empty positions available, check if the game is a tie 
            print("Keine leeren Positionen mehr!")
            
            
