class BaseAgent:

    def __init__(self, name, balance = 100):

        self.name = name
        self.balance = balance

        self.total_profit = 0
        self.wins = 0
        self.total_spent = 0
        self.total_profit = 0
        self.failed_bids = 0

        self.bid_history = []
        self.profit_history = []

    def place_bid(self, item):
        
        raise NotImplementedError("Subclasses must implement place_bid()")

    def is_valid_bid(self, bid, current_highest_bid, minimum_bid = 1):

        # bid must meet min value
        if bid < minimum_bid:
            return False
        
        # bid must exceed current value
        if bid <= current_highest_bid:
            return False
        
        # cannot spend more than available balance
        if bid > self.balance:
            return False
        
        return True
    
    def update_profit(self, profit):
        
        self.total_profit += profit
        self.profit_history.append(profit)

    def record_bid(self, bid):
        
        self.bid_history.append(bid)

    def record_win(self):
        
        self.wins += 1

    def record_failed_bid(self):

        self.failed_bids += 1

    def get_win_rate(self, total_rounds):
        
        if total_rounds == 0:
            return 0

        return self.wins / total_rounds