import random

from agents.base_agent import BaseAgent

class ConservativeAgent(BaseAgent):
    
    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):
        
        if current_highest_bid >= item.true_value:
            return 0
        
        minimum_bid = current_highest_bid + 1
        maximum_bid = min(current_highest_bid + 5, item.true_value, self.balance)
        
        # prevent invalid ranges
        if minimum_bid > maximum_bid:
            self.record_failed_bid()
            return 0

        bid = random.randint(minimum_bid, maximum_bid)
        
        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0
        
        # record bid stats
        self.record_bid(bid)

        if memory:
            memory.round_history.append({
                "agent": self.name,
                "round": current_round,
                "bid": bid,
                "result": "submitted"
            })

        return bid