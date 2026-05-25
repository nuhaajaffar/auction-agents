from agents.base_agent import BaseAgent

class FixedAgent(BaseAgent):

    def __init__(self, name = "Fixed", balance = 100, fixed_bid = 60):

        super().__init__(name, balance)
        self.fixed_bid = fixed_bid

    def place_bid(self, item, current_highest_bid = 0, current_round = 1, max_rounds = 5, memory = None):

        perceived_value = self.get_item_value(item)

        if current_highest_bid >= perceived_value:
            return 0

        bid = self.fixed_bid

        if bid <= current_highest_bid:
            bid = current_highest_bid + 1

        if bid > perceived_value or bid > self.balance:
            self.record_failed_bid()
            return 0

        if not self.is_valid_bid(bid, current_highest_bid):
            self.record_failed_bid()
            return 0

        self.record_bid(bid)

        self.log_memory(memory, {
            "agent": self.name,
            "round": current_round,
            "bid": bid,
            "result": "submitted",
            "perceived_value": perceived_value,
            "true_value": item.true_value
        })

        return bid