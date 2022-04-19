import numpy as np

class statistics:
    def __init__(self, data, percentile = 2.5):
        # remove some data to avoid a result "ruined" by a few mistakes
        if len(data) >= 10:
            data = sorted(data)
            remove = min([len(data) // 10, 5])
            self.values = data[remove:-remove]
        else:
            self.values = data
        
        self.n = len(self.values)
        self.mean = np.mean(self.values)
        sqsum = sum([(x - self.mean) ** 2 for x in self.values])
        self.variance = sqsum / self.n
        self.std = np.sqrt(sqsum / (self.n - 1))
        self.perc = percentile
        self.lowperc = np.percentile(self.values, percentile)
        self.upperc = np.percentile(self.values, 100 - percentile)