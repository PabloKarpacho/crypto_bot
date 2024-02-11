import pandas as pd
from config import api_key, secret
from pybit.unified_trading import HTTP



class get_candels:
    def __init__(self, category = "spot", symbol = "BTCUSDT", interval = 1, limit = 60):

        self.session = HTTP(api_key=api_key, api_secret=secret, testnet=False)

        self.category = category
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

    def getting_server_time(self):

        current_time = pd.to_datetime(int(self.session.get_server_time().get('result')['timeSecond']), unit='s')
        self.current_time_without_seconds = int(current_time.replace(second=0, microsecond=0).timestamp()) * 1000

    def get_response(self):

        self.getting_server_time()

        if self.interval in [1,3,5,15,30,60,120,240,360,720]:
            time_koef = 60
            time_inteval = self.interval
        
        elif self.interval == 'D':
            time_koef = 86400
            time_inteval = 1
        
        elif self.interval == 'W':
            time_koef = 86400 * 7
            time_inteval = 1
        
        elif self.interval == 'M':
            time_koef = 86400 * 30
            time_inteval = 1
        
        else:
            raise ValueError(f'Invalid interval: {self.interval}')

        response = self.session.get_kline(
        category=self.category,
        symbol=self.symbol,
        interval=self.interval,
        start=(self.current_time_without_seconds/1000 -  time_inteval * self.limit * time_koef) * 1000,
        end=self.current_time_without_seconds, limit = 1000
        ).get('result')

        return response
    
    def getting_data(self):

        response = self.get_response()
        
        data = pd.DataFrame(response['list'])

        data.rename(columns= {0 : 'time',   
                      1:"open",
                      2: "high",
                      3: "low",
                      4: "close",
                      5 : "volume",
                      6: "turnover"}, inplace=True)
        
        data['time'] = data['time'].apply(lambda x: pd.to_datetime(int(x[:-3]), unit='s'))

        data[["open", "high", "low", "close", "volume", "turnover"]] = data[["open", "high", "low", "close", "volume", "turnover"]].astype(float)

        data['date'] = data['time'].dt.date

        data.sort_values(by='time', ignore_index=True, inplace=True)

        # data.set_index(data['time'], inplace=True)

        return data