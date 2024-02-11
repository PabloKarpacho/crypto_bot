
class MAKD_Strategy:
    def __init__(self, fastperiod = 12, slowperiod = 26, signalperiod = 9):
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod
    
    def get_bounds(self, fastperiod = (2, 30), slowperiod = (2, 30), signalperiod = (2,30)):

        self.bounds = {'fastperiod' : fastperiod,
                       'slowperiod' : slowperiod,
                       'signalperiod' : signalperiod}
    
class RSI_Strategy:
    def __init__(self, rsi = 14, rsi_low = 30, rsi_high = 70):
        self.rsi = rsi
        # self.rsi_low = rsi_low
        # self.rsi_high = rsi_high

    def get_bounds(self, rsi = (2, 30), rsi_low = (25, 40), rsi_high = (65, 80)):

        self.bounds = {'rsi' : rsi,
                        # 'rsi_low' : rsi_low,
                        # 'rsi_high' : rsi_high
                        }

class Take_profit:
    def __init__(self, revenue = 1):
        self.revenue = revenue
    
    def get_bounds(self, revenue = (1, 5)):
        self.bounds = {'revenue' : revenue,

                      }

class StopLoss:
    def __init__(self, loss = -1):
        self.loss = loss
    
    def get_bounds(self, loss = (-3, -1)):
        self.bounds = {'loss' : loss,

                      }
    
