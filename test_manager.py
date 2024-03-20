# Important! Only for testing winning-screen & update-settings functionality!

import numpy as np
import json

class manager():

    def __init__(self):
        pass

    def is_winner(self, board_status, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if board_status[i][0] == board_status[i][1] == board_status[i][2] == player:
                return True
            if board_status[0][i] == board_status[1][i] == board_status[2][i] == player:
                return True

        # Diagonals
        if board_status[0][0] == board_status[1][1] == board_status[2][2] == player:
            return True

        if board_status[0][2] == board_status[1][1] == board_status[2][0] == player:
            return True

        return False

    def is_tie(self, board_status):

        r, c = np.where(board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def checkboard(self, board_status, player):
        if player:
            player = "X"
        else:
            player = "O"
        answer = self.is_winner(board_status, player)
        answer2 = self.is_tie(board_status)
        if answer:
            return player
        elif answer2:
            return "Tie"
        
    def update_stats(self, stat):

        with open("own_stats_example.json", "r") as f:
            data_own = json.load(f)

            if stat == "X":
                wins = int(data_own["wins"])
                wins +=1
                data_own["wins"] = str(wins)
            elif stat == "O":
                losses = int(data_own["losses"])
                losses +=1
                data_own["losses"] = str(losses)
            elif stat == "Tie":
                tie = int(data_own["draws"])
                tie +=1
                data_own["draws"] = str(tie)

        with open("own_stats_example.json", "w") as f:
            f.write(json.dumps(data_own))