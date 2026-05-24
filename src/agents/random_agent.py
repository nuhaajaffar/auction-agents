import random

from agents.base_agent import BaseAgent

class RandomAgent(BaseAgent):

    def place_bid(self, item, current_highest_bid = 0):
        
        if current_highest_bid >= item.true_value:
            return 0
        
        minimum_bid = current_highest_bid + 1
        maximum_bid = item.true_value

        if minimum_bid > maximum_bid:
            return 0

        bid = random.randint(minimum_bid, maximum_bid)

        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0

        # record bid stats
        self.record_bid(bid)

        return bid