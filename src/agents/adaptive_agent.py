import random

from agents.base_agent import BaseAgent

class AdaptiveBidder(BaseAgent):

    def __init__(self, name = "Adaptive", balance = 100):

        super().__init__(name, balance)
        self.aggressiveness = 1.0

    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):

        if current_highest_bid >= item.true_value:
            return 0

        # get market signals
        market_avg = memory.get_market_average()
        volatility = memory.get_market_volatility()
        pressure = memory.estimate_market_pressure()
        competition = memory.estimate_competition()

        # base bid logic
        base_value = item.true_value * 0.6  # conservative base

        # market adjustment
        market_factor = 1 + (market_avg - item.true_value) / 100

        # pressure adjustment
        if pressure == "HIGH":
            pressure_factor = 1.3
        elif pressure == "COMPETITIVE":
            pressure_factor = 1.1
        else:
            pressure_factor = 0.9

        # volatility adjustment
        volatility_factor = 1 + (volatility / 100)

        # competition adjustment
        competition_factor = 1 + competition * 0.5

        # aggressiveness adaptation
        if current_round > max_rounds * 0.7:
            self.aggressiveness += 0.05
        else:
            self.aggressiveness *= 0.98  # slowly calm down

        self.aggressiveness = max(0.7, min(1.5, self.aggressiveness))

        # final bid calculation
        bid = base_value
        bid *= market_factor
        bid *= pressure_factor
        bid *= volatility_factor
        bid *= competition_factor
        bid *= self.aggressiveness

        # clamp bid
        minimum_bid = current_highest_bid + 1
        maximum_bid = item.true_value

        bid = max(minimum_bid, min(bid, maximum_bid))

        bid = int(bid)

        # validation + recording
        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0

        self.record_bid(bid)

        return bid