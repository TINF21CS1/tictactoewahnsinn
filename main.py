from actors.user import User
from actors.user import Opponent

def main():
    x = User("Test")
    print(x)
    x._update_statistics("loss")
    print(x)
    y= Opponent("test")
    print(y)
    y._update_statistics("win")
    print(y)

main()
