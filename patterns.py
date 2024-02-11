class patterns:
    def __init__(self, data):
        self.data = data

    def check_pattern(self, pattern, i):
        points = 0 
        if self.data[pattern].loc[i] == 100:
            points += 1
        elif self.data[pattern].loc[i] == -100:
            points -= 1
        elif self.data[pattern].loc[i] == 0:
            pass

        return points