import json
import uuid

class user():
    def __init__(self, name: str):
        self._name = name
        self._id = uuid.uuid4()
        self._wins = 0
        self._draws = 0
        self._losses = 0

    @classmethod
    def user_from_data(cls, data): 
        with open('user_data.json', 'r') as user_data:
            data=user_data.read()
    
    def __str__(self):
        return f"{self._name} {self._id} {self._wins} {self._draws} {self._losses}"

    def updateStatistics(self): 
        pass



x = user("test")
print(x)

            
    

