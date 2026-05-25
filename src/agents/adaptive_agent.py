import random

from agents.base_agent import BaseAgent

class AdaptiveAgent(BaseAgent):

    def __init__(self, name = "Adaptive Agent", balance = 100, use_memory = True):

        super().__init__(name, balance)
        self.use_memory = use_memory
        self.aggressiveness = 1.0
        self.aggressiveness_history = []
        self.bid_factor_history = []

    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):

        if current_highest_bid >= item.true_value:
            return 0

        base_value = item.true_value * 0.6

        if self.use_memory and memory is not None:        
            
            # market signals
            market_avg = memory.get_market_average()
            volatility = memory.get_market_volatility()
            pressure = memory.estimate_market_pressure()
            competition = memory.estimate_competition()

            # market adjustment
            market_factor = 1 + (market_avg - item.true_value) / 100
            market_factor = max(0.6, min(1.4, market_factor))

            # pressure adjustment
            if pressure == "HIGH":
                pressure_factor = 1.3
            elif pressure == "COMPETITIVE":
                pressure_factor = 1.1
            else:
                pressure_factor = 0.9

            # volatility adjustment
            volatility_factor = 1 + (volatility / 100)
            volatility_factor = max(1.0, min(1.3, volatility_factor))
            
            # competition adjustment
            competition_factor = 1 + (competition * 0.5)

            overpay_factor = self.get_overpay_factor(memory)
        else:
            market_avg = 0
            volatility = 0
            pressure = "NO_MEMORY"
            competition = 0

            market_factor = 1.0
            pressure_factor = 1.0
            volatility_factor = 1.0
            competition_factor = 1.0
            overpay_factor = 1.0

        # final bid calculation
        bid = base_value
        bid *= market_factor
        bid *= pressure_factor
        bid *= volatility_factor
        bid *= competition_factor
        bid *= overpay_factor
        bid *= self.aggressiveness

        # clamp bid
        minimum_bid = current_highest_bid + 1
        maximum_bid = min(item.true_value, self.balance)

        if minimum_bid > maximum_bid:
            self.record_failed_bid()
            return 0
    
        bid = max(minimum_bid, min(bid, maximum_bid))

        bid = int(bid)

        # validation + recording
        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0

        self.record_bid(bid)

        # update learning
        if self.use_memory and memory is not None:
            self.update_aggressiveness(memory)

        self.aggressiveness_history.append(self.aggressiveness)

        self.bid_factor_history.append({
            "round": current_round,
            "bid": bid,
            "aggressiveness": self.aggressiveness,
            "memory_access": self.use_memory,
            "market_average": market_avg,
            "volatility": volatility,
            "pressure": pressure,
            "competition": competition
        })

        memory_status = "memory" if self.use_memory else "no memory"

        print(
            f"{self.name} | Round {current_round} | "
            f"Bid: {bid} | Agg: {self.aggressiveness:.2f} | {memory_status}"
        )

        return bid

    # learning mechanism
    def update_aggressiveness(self, memory):

        if len(memory.losing_bids) > len(memory.winning_bids):
            self.aggressiveness += 0.05
        else:
            self.aggressiveness -= 0.03

        # clamp to safe range
        self.aggressiveness = max(0.7, min(1.2, self.aggressiveness))

    def get_overpay_factor(self, memory):

        if len(memory.winning_bids) < 2:
            return 1.0

        recent_wins = memory.winning_bids[-5:]
        avg_win_price = sum(recent_wins) / len(recent_wins)

        if avg_win_price > 90:
            return 0.85
        elif avg_win_price < 50:
            return 1.05
        else:
            return 1.0