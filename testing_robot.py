class robot:
    def __init__(self, cash):
        self.cash = cash
        self.qty = 0
    
    def buy(self, qty, price):
        self.qty += qty
        self.cash -= price*qty
    
    def sell(self, qty, price):
        self.qty -= qty
        self.cash += price*qty