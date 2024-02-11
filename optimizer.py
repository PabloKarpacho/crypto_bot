import optuna
from testing_robot import robot
from united_dfs import united_dfs
from get_candels import get_candels
from calculate_ta_indicators import calculate_ta_indicators
from patterns import patterns
from ta_strategies import MAKD_Strategy, RSI_Strategy, Take_profit, StopLoss
import copy


class optimization:

    def __init__(self, intervals = [1,3], limit = 999, category = "spot", symbol = "BTCUSDT", indicators = [MAKD_Strategy, RSI_Strategy], backtest = False, SL = False, TP = False):
        
        self.intevals = intervals
        for i in self.intevals:
            setattr(self, f"interval_{i}", i)
    
        self.limit = limit
        self.category = category
        self.symbol = symbol
        self.indicators = indicators
        self.stop_rev = {}
        if SL:
            sl = StopLoss()
            sl.get_bounds()
            self.stop_rev['loss'] = sl.bounds
        else: 
            self.stop_rev['loss'] = None

        if TP:
            tp = Take_profit()
            tp.get_bounds()
            self.stop_rev['revenue'] = tp.bounds
        else:
            self.stop_rev['revenue'] = None


        self.indicator_names = [x.__name__ for x in self.indicators]

        self.backtest = backtest

    def get_data(self):

        for i in self.intevals:
            candels_downloader = get_candels(interval = getattr(self, f"interval_{i}"), limit = self.limit, category = self.category, symbol = self.symbol)
            setattr(self, f"data_{i}", candels_downloader.getting_data())

    def objective(self, trial):

        if self.backtest:
                
            ind_values = {}

            for indicator in self.indicators:
                values = {}
                for i in self.intevals:
                    ind = indicator()
                    values[f"{ind.__class__.__name__}_{i}"] = ind.__dict__
                
                ind_values[f"{indicator.__name__}"] = values

        else:
            ind_values = {}

            for indicator in self.indicators:
                values = {}

                for k in self.intevals:
                    ind = indicator()
                    params = copy.deepcopy(ind.__dict__)
                    ind.get_bounds()
                    bounds = ind.bounds

                    for key in params.keys():
                        params[key] = trial.suggest_int(f"{key}_{k}", bounds[key][0] , bounds[key][1])

                    values[f"{ind.__class__.__name__}_{k}"] = copy.deepcopy(params)
                
                ind_values[f"{indicator.__name__}"] = values

       

        if self.stop_rev:
            for key in self.stop_rev.keys():
                bounds = self.stop_rev[key]
                if bounds:
                    params[key] = trial.suggest_int(f"{key}", bounds[key][0] , bounds[key][1])

        periods = [] 

        for i in self.intevals:
            data = copy.deepcopy(getattr(self, f"data_{i}"))
            self.params_ = {}

            for key in ind_values.keys():
                needed_key = [x for x in ind_values[key].keys() if str(i) in x][0]
         
                for k,v in ind_values[key][needed_key].items():
                    self.params_[k] = v



            indicators_data = calculate_ta_indicators(data, **self.params_)
            periods.append(united_dfs(data, indicators_data))


        qty = 1
        init_sum = 100000
        bot = robot(cash=init_sum)

        # pattern_list = ['hammer', 'shooting_star', 'evening_star', 'morning_star', 'piersing', 'three_white_soldiers', 'three_black_crowns', 'hanging_man', 'dark_cloud_clover']

        open_p = []
        open_d = []

        close_p = []
        close_d = []

        transactions = 0
        mistakes = 0

        comission = 0.001

        buy = False
        sell = True

        small_period = periods[0]

        for i in range(len(small_period) - 3):
            points = 0 

            for period in periods:

                if period is small_period:
                    per_1 = period.loc[i+1]
                    per_2 = period.loc[i+2]
                    per_3 = period.loc[i+3]


                    MAKD = MAKD_Strategy.__name__
       

                    if MAKD in self.indicator_names:
                        if per_1['macdhist'] < 0 and per_2['macdhist'] > 0:
                            points += 1
                        elif per_1['macdhist'] > 0 and per_2['macdhist'] < 0:
                            points -= 1

                    RSI = RSI_Strategy.__name__
           
                    if RSI in self.indicator_names:
                        if (per_3['rsi'] <= 30):
                            points += 1
                            if self.backtest:
                                print(f"rsi + : {points}")
                        elif (per_3['rsi'] >= 70):
                            points -= 1
                            if self.backtest:
                                print(f"rsi - : {points}")
                    
                    if (self.stop_rev['revenue']) and (not sell):
                        price = small_period['open'].loc[i+3]

                        if (b_p - price)/b_p * 100 >= params['revenue']:
                            points += 1

                    if (self.stop_rev['loss']) and (buy):
                        price = small_period['open'].loc[i+3]

                        if (b_p - price)/b_p * 100 <= params['loss']:
                            points -= 1


             

                
                else:
                    per_1 = period[period['time'] <= small_period['time'].loc[i+3]].iloc[-1]
                    per_2 = period[period['time'] <= small_period['time'].loc[i+3]].iloc[-2]
                    per_3 = period[period['time'] <= small_period['time'].loc[i+3]].iloc[-3]

                    if MAKD in self.indicator_names:
                        if (per_1['macd_diff'] > 0) and (per_2['macd_diff'] < 0) and (per_1['macdhist'] > 0) and (per_2['macdhist'] > 0):
                            points-= 1
                            if self.backtest:
                                print(f"macd_diff - : {points}")
                        elif (per_1['macd_diff'] < 0) and (per_2['macd_diff'] > 0) and (per_1['macdhist'] < 0) and (per_2['macdhist'] < 0):
                            points+= 1
                            if self.backtest:
                                print(f"macd_diff + : {points}")

                        if (per_1['macdhist'] <= per_2['macdhist']) and (per_1['macdhist'] > 0) and (per_2['macdhist'] > 0):
                            points += 1
                            if self.backtest:
                                print(f"macd_diff + exp : {points}")
                        elif (per_1['macdhist'] >= per_2['macdhist']) and (per_1['macdhist'] < 0) and (per_2['macdhist'] < 0):
                            points += 1
                            if self.backtest:
                                print(f"macd_diff + exp : {points}")
            
    
                # if buy:
                #     if (s_p - b_p - (s_p + b_p)*comission) / b_p > 0.1:
                #         points -= 1
                #         if backtest:
                #             print(f"cond : {points}, rev: {(s_p - b_p - (s_p + b_p)*comission) / b_p * 100}")


                # pat_checker_small = patterns(small_period)

                # for pattern in pattern_list:
                #     points += pat_checker_small.check_pattern(pattern, i+1)
                #     points += pat_checker_small.check_pattern(pattern, i+2)
                #     if backtest:
                #         print(f"pattern {points}")
                            
            
            
            if (points > 0) and (not buy):
                b_p = small_period['open'].loc[i+3]
                bot.buy(qty=qty, price=b_p)
        
                bot.cash -= b_p * comission

                if self.backtest:
                    print(f'buy price {b_p} buy_date {small_period["time"].loc[i+3]}')

                open_p.append(b_p)
                open_d.append(small_period["time"].loc[i+3])
                
                buy = not buy
                sell = not sell
                
            if (points) < 0 and (not sell):
                s_p = small_period['open'].loc[i+3]
                bot.sell(qty=qty, price=s_p)
                bot.cash -= s_p * comission

                buy = not buy
                sell = not sell 

                transactions += 1
                revenue = (s_p - b_p - (s_p + b_p)*comission) / b_p * 100
                if revenue < 0:
                    mistakes+=1
                if self.backtest:
                    print(f'sell price {s_p} sell_date {small_period["time"].loc[i+3]}')

                    print(f"Прибыль {revenue} %, Остаток {bot.cash}")

                    print(f"transactions/mistakes: {transactions}/{mistakes}")

                close_p.append(s_p)
                close_d.append(small_period["time"].loc[i+3])

        self.buy = {'time' : open_d, 'buy_price' : open_p}
        self.sell = {'time' : close_d, 'sell_price' : close_p}
        self.transactions = transactions
        self.mistakes = mistakes
    
        return (bot.qty * small_period['open'].loc[i+3] + bot.cash - init_sum)/init_sum *100

    
    
    def optimize(self, n_trials=100):
 
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=n_trials)

        return study

