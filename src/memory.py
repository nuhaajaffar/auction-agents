class Memory:

    def __init__(self):
        
        self.winning_bids = []
        self.losing_bids = []
        self.market_prices = []
        self.round_history = []
        self.competitor_strength = 0.5 # default neutral value
        
    def update_win(self, agent_name, bid, price, round_id = None):
        
        self.winning_bids.append(bid)
        self.market_prices.append(bid)

        self.round_history.append({
            "round": round_id,
            "agent": agent_name,
            "result": "win",
            "bid": bid,
            "price": price
        })

    def update_loss(self, agent_name, bid, price, round_id = None):

        self.losing_bids.append(bid)

        self.round_history.append({
            "round": round_id,
            "agent": agent_name,
            "result": "loss",
            "bid": bid,
            "price": price
        })

    def get_market_average(self):

        if len(self.market_prices) == 0:
            return 50

        recent = self.market_prices[-10:]
        return sum(recent) / len(recent)
    
    def get_market_volatility(self):

        if len(self.market_prices) < 2:
            return 0

        recent = self.market_prices[-10:]
        avg = sum(recent) / len(recent)
        variance = sum((p - avg) ** 2 for p in recent) / len(recent)

        return variance ** 0.5

    def estimate_market_pressure(self):

        avg = self.get_market_average()
        volatility = self.get_market_volatility()

        if volatility > 20:
            return "HIGH"
        elif avg > 100:
            return "COMPETITIVE"
        else:
            return "NORMAL"
        
    def estimate_competition(self):

        if len(self.market_prices) < 3:
            return 0.5

        recent = self.market_prices[-5:]
        avg = sum(recent) / len(recent)

        if avg > 100:
            return 0.9
        elif avg > 60:
            return 0.6
        else:
            return 0.3