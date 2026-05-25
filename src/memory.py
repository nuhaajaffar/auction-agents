class Memory:

    def __init__(self):
        
        self.winning_bids = []
        self.losing_bids = []
        self.market_prices = []
        self.round_history = []
        self.competitor_strength = 0.5 # default neutral value
        
    def update_win(self, bid, price, round_id = None):
        
        self.winning_bids.append(price)
        self.market_prices.append(price)

        self.round_history.append({
            "round": round_id,
            "result": "win",
            "bid": bid,
            "price": price
        })

    def update_loss(self, bid, price, round_id = None):

        self.losing_bids.append(bid)
        self.market_prices.append(price)

        self.round_history.append({
            "round": round_id,
            "result": "loss",
            "bid": bid,
            "price": price
        })