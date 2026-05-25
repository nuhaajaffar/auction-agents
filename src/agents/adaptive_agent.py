import random

from agents.base_agent import BaseAgent

class AdaptiveAgent(BaseAgent):

    def __init__(self, name = "Adaptive", balance = 100):

        super().__init__(name, balance)
        self.aggressiveness = 1.0
        self.aggressiveness_history = []

    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):

        if current_highest_bid >= item.true_value:
            return 0

        # get market signals
        market_avg = memory.get_market_average()
        volatility = memory.get_market_volatility()
        pressure = memory.estimate_market_pressure()
        competition = memory.estimate_competition()

        # base bid logic
        base_value = item.true_value * 0.55  # conservative base

        # market adjustment
        market_factor = 1 + (market_avg - base_value) / 200

        # pressure adjustment
        if pressure == "HIGH":
            pressure_factor = 0.95
        elif pressure == "COMPETITIVE":
            pressure_factor = 1.05
        else:
            pressure_factor = 1.0

        # volatility adjustment
        volatility_factor = max(0.85, 1 - (volatility / 200))

        # competition adjustment
        if competition > 0.7:
            competition_factor = 1.15
        elif competition < 0.4:
            competition_factor = 0.9
        else:
            competition_factor = 1.0

        overpay_factor = self.get_overpay_factor(memory)

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
        self.update_aggressiveness(memory)

        print(
            f"{self.name} | Round {current_round} | "
            f"Bid: {bid} | Agg: {self.aggressiveness:.2f}"
        )

        return bid

    # learning mechanism
    def update_aggressiveness(self, memory):

        if len(memory.losing_bids) > len(memory.winning_bids):
            self.aggressiveness += 0.04
        else:
            self.aggressiveness -= 0.03

        # clamp to safe range
        self.aggressiveness = max(0.7, min(1.2, self.aggressiveness))
        self.aggressiveness_history.append(self.aggressiveness)

    def get_overpay_factor(self, memory):

        if len(memory.winning_bids) < 2:
            return 1.0

        recent_wins = memory.winning_bids[-5:]
        avg_win_price = sum(recent_wins) / len(recent_wins)

        if avg_win_price > 100:
            return 0.8
        elif avg_win_price > 80:
            return 0.9
        elif avg_win_price < 50:
            return 1.05
        else:
            return 1.0