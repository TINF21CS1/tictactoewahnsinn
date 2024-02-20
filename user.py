import json
import uuid
from abc import ABC, abstractmethod
import os

class Player():
    def __init__(self, name: str, wins=0, draws=0, losses=0, id=uuid.uuid4()):
        self._name = name
        self._id = uuid.uuid4()
        self._wins = wins 
        self._draws = draws 
        self._losses = losses
    
    @abstractmethod
    def make_move(self):
        pass

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_wins(self):
        return self._wins

    def get_draws(self):
        return self._draws

    def get_losses(self):
        return self._losses

    def __str__(self):
        return f"{self._name} {self._id} {self._wins} {self._draws} {self._losses}"

    
    

        
class User(Player):
    @classmethod
    def from_data(cls): 
        with open('user_data.json', 'r') as user_data:
            data=json.load(user_data)
        name = data["name"]
        id = data["id"]
        wins = data["wins"]
        draws = data["draws"]
        losses = data["losses"]

        return cls(name, wins, draws, losses, id)

    def _save_data(self):
        with open("user_data.json", "w") as user_data:
            json.dump({"name": self._name, "id": str(self._id), "wins": self._wins, "draws": self._draws, "losses": self._losses}, user_data) 

    def change_name(self, name):
        self._name = name
        self._save_data()

    def make_move(self):
        pass

    def delete_profile(self):
        os.remove("user_data.json")

    def _updateStatistics(self, status: str): 
        match status:
            case "win":
                self._wins+=1
            case "draw":
                self._draws+=1
            case "loss":
                self._losses+=1
        self._save_data()


class Opponent(Player):
    pass


x = User("hallo")
print(x)
x._updateStatistics("loss")
print(x)
y = Opponent("gegner")
x.change_name("absoluter boss")   
print(x)
x.delete_profile()
print(x)
