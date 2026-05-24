class BaseAgent:

    def __init__(self, name):

        self.name = name

        self.total_profit = 0
        self.wins = 0

        self.bid_history = []
        self.profit_history = []

    def place_bid(self, item):
        
        raise NotImplementedError("Subclasses must implement place_bid()")

    def update_profit(self, profit):
        
        self.total_profit += profit
        self.profit_history.append(profit)

    def record_bid(self, bid):
        
        self.bid_history.append(bid)

    def record_win(self):
        
        self.wins += 1

    def get_win_rate(self, total_rounds):
        
        if total_rounds == 0:
            return 0

        return self.wins / total_rounds