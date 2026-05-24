import random

from agents.base_agent import BaseAgent

class RandomAgent(BaseAgent):

    def place_bid(self, item):

        bid = random.randint(1, item.true_value)

        self.record_bid(bid)

        return bid