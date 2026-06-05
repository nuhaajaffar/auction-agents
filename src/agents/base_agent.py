# parent class

class BaseAgent:

    def __init__(self, name, balance = 100):

        self.name = name
        self.balance = balance

        self.wins = 0
        self.total_spent = 0
        self.total_profit = 0
        self.failed_bids = 0

        self.bid_history = []
        self.profit_history = []

    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):

        raise NotImplementedError("Subclasses must implement place_bid()")
    
    def get_item_value(self, item):

        return getattr(item, "perceived_value", item.true_value)

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

    def record_bid(self, bid):

        self.bid_history.append(bid)

    def record_win(self):

        self.wins += 1

    def record_failed_bid(self):

        self.failed_bids += 1

    def update_profit(self, profit):

        self.total_profit += profit
        self.profit_history.append(profit)

    def get_average_bid(self):

        if len(self.bid_history) == 0:
            return 0

        return sum(self.bid_history) / len(self.bid_history)

    def get_win_rate(self, total_rounds):

        if total_rounds == 0:
            return 0

        return self.wins / total_rounds

    def log_memory(self, memory, data):

        if memory is not None:
            memory.round_history.append(data)