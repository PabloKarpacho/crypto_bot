import pandas as pd
from talib import abstract


class calculate_ta_indicators:
    def __init__(self, data, fastperiod=12, slowperiod=26, signalperiod=9, rsi = 12, bollinger = 20, aroon_osc = 12, linreg = 14, price = 'open'):
        # self.sma_1 = abstract.SMA(data, timeperiod=12)
        # self.sma_2 = abstract.SMA(data, timeperiod=26)
        self.macd = abstract.MACD(data, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod, price = price)
        self.macd['macd_diff'] = self.macd['macdhist'].diff()
        self.rsi = pd.DataFrame({'rsi' : abstract.RSI(data, timeperiod=rsi, price = price)})
        self.bollinger = abstract.BBANDS(data, timeperiod = bollinger, price = price)
        self.aroon_osc = pd.DataFrame({'aroon_osc' : abstract.AROONOSC(data, n = aroon_osc, price = price)})

        self.linearreg_angle = abstract.LINEARREG_ANGLE(data, timeperiod=linreg, price = price)

        self.hammer = pd.DataFrame({'hammer' : abstract.CDLHAMMER(data)})
        self.shooting_star = pd.DataFrame({'shooting_star' : abstract.CDLSHOOTINGSTAR(data)})
        self.evening_star = pd.DataFrame({'evening_star' : abstract.CDLEVENINGSTAR(data)})
        self.morning_star = pd.DataFrame({'morning_star' : abstract.CDLMORNINGSTAR(data)})
        self.piersing = pd.DataFrame({'piersing' : abstract.CDLPIERCING(data)})
        self.three_white_soldiers = pd.DataFrame({'three_white_soldiers' : abstract.CDL3WHITESOLDIERS(data)})
        self.three_black_crowns = pd.DataFrame({'three_black_crowns' : abstract.CDL3BLACKCROWS(data)})
        self.hanging_man = pd.DataFrame({'hanging_man' : abstract.CDLHANGINGMAN(data)})
        self.dark_cloud_clover = pd.DataFrame({'dark_cloud_clover' : abstract.CDLDARKCLOUDCOVER(data)})