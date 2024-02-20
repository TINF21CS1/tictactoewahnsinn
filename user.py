import json
import uuid

class user():
    def __init__(self, name: str, wins=0, draws=0, losses=0, id=uuid.uuid4()):
        self._name = name
        self._id = uuid.uuid4()
        self._wins = wins 
        self._draws = draws 
        self._losses = losses
        self.save_data()
        
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
    
    def __str__(self):
        return f"{self._name} {self._id} {self._wins} {self._draws} {self._losses}"

    def updateStatistics(self, status: str): 
        match status:
            case "win":
                self._wins+=1
            case "draw":
                self._draws+=1
            case "loss":
                self._losses+=1
        self.save_data()

    def save_data(self):
        with open("user_data.json", "w") as user_data:
            json.dump({"name": self._name, "id": str(self._id), "wins": self._wins, "draws": self._draws, "losses": self._losses}, user_data) 


    

# x = user("test")
x = user.from_data()
print(x)
x.updateStatistics("loss")
print(x)

            
    

