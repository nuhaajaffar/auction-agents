import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from environment.auction_environment import AuctionEnvironment
from agents.fixed_agent import FixedAgent
from agents.adaptive_agent import AdaptiveAgent
from memory import Memory

def run_learning_test():

    print("\n===== LEARNING BEHAVIOUR TEST =====")

    memory = Memory()

    fixed_agent = FixedAgent("Fixed Agent", balance = 1500, fixed_bid = 60)
    adaptive_agent = AdaptiveAgent("Adaptive Agent", balance = 1500)

    agents = [fixed_agent, adaptive_agent]

    env = AuctionEnvironment(
        agents = agents,
        memory = memory,
        num_rounds = 30
    )

    env.run_simulation()

run_learning_test()