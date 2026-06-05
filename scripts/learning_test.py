import sys
import os
import json
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from environment.auction_environment import AuctionEnvironment
from agents.fixed_agent import FixedAgent
from agents.adaptive_agent import AdaptiveAgent
from memory import Memory

def run_learning_test():
    
    random.seed(5000)

    print("\n===== LEARNING BEHAVIOUR TEST =====")

    memory = Memory()

    fixed_agent = FixedAgent("Fixed Agent", balance = 1500, fixed_bid = 60)
    adaptive_agent = AdaptiveAgent("Adaptive Agent", balance = 1500)
    
    agents = [fixed_agent, adaptive_agent]

    env = AuctionEnvironment(
        agents=agents,
        memory=memory,
        num_rounds = 30
    )

    env.run_simulation()

    learning_results = {
        "adaptive_agent": {
            "wins": adaptive_agent.wins,
            "total_profit": adaptive_agent.total_profit,
            "average_bid": round(adaptive_agent.get_average_bid(), 2),
            "failed_bids": adaptive_agent.failed_bids,
            "aggressiveness_history": adaptive_agent.aggressiveness_history
        },
        "fixed_agent": {
            "wins": fixed_agent.wins,
            "total_profit": fixed_agent.total_profit,
            "average_bid": round(fixed_agent.get_average_bid(), 2),
            "failed_bids": fixed_agent.failed_bids
        }
    }

    os.makedirs("results", exist_ok=True)

    with open("results/learning_metrics.json", "w") as f:
        json.dump(learning_results, f, indent = 4)

    print("\nLearning metrics exported successfully.")

if __name__ == "__main__":
    run_learning_test()