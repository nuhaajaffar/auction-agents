import random

from agents.base_agent import BaseAgent

class AggressiveAgent(BaseAgent):

    def place_bid(self, item, current_highest_bid):
        
        if current_highest_bid >= item.true_value:
            return 0
        
        minimum_bid = current_highest_bid + 10
        maximum_bid = min(current_highest_bid + 25, item.true_value)

        # prevent invalid ranges
        if minimum_bid > maximum_bid:
            minimum_bid = current_highest_bid + 1

        bid = random.randint(minimum_bid, maximum_bid)

        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0
        
        # record bid stats
        self.record_bid(bid)

        return bid