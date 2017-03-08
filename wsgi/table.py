from collections import defaultdict

class Table:
    def __init__(self, stake=100):
        self.bets = defaultdict(int)
        self.stake = stake

    def place_bet(self, name , amount):
        self.bets[name] += amount

    def clear_bet(self, name):
        del self.bets[name]

    def clear_bets(self):
        self.bets = defaultdict(int)

    def resolve(self, spin):
        wins = []
        loses = []
        while self.bets:
            bet, amount = self.bets.popitem()
            if bet in spin:
                x, y = spin[bet]
                self.stake += amount * x // y
                wins.append((bet, amount, "win"))
            else:
                self.stake -= amount
                loses.append((bet, amount, "lose"))
        return (wins, loses)

    def available(self):
        return self.stake

from rest_client import *
from random import randint
if __name__ == "__main__":
    wins = []
    loses = []
    table = Table()
    a = [randint(0,36) for _ in range(15)]
    for _ in range(10):
        for i in a:
            table.place_bet(str(i),2)
        #in this stage the server of wsgi must be running
        #to reveive requests
        win, lose = table.resolve(json_get())
        wins += win
        loses += lose
    print("*** Wins ***\n")
    for w in wins:
        print(w)
    print("*** Loses ***\n")
    for l in loses:
        print(l)
    print(table.available())
    
    
