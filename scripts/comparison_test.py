import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from environment.auction_environment import AuctionEnvironment
from agents.fixed_agent import FixedAgent
from agents.random_agent import RandomAgent
from agents.adaptive_agent import AdaptiveAgent
from memory import Memory

def run_comparison_test():

    print("\n===== AGENT COMPARISON TEST =====")

    memory = Memory()

    fixed_agent = FixedAgent(
        "Fixed Agent",
        balance = 1500,
        fixed_bid = 60
    )

    random_agent = RandomAgent(
        "Random Agent",
        balance = 1500
    )

    adaptive_agent = AdaptiveAgent(
        "Adaptive Agent",
        balance = 1500
    )

    agents = [
        fixed_agent,
        random_agent,
        adaptive_agent
    ]

    env = AuctionEnvironment(
        agents=agents,
        memory=memory,
        num_rounds = 30
    )

    env.run_simulation()

    comparison_results = []

    for agent in agents:

        win_rate = agent.get_win_rate(30) * 100

        if agent.total_spent == 0:
            bid_efficiency = 0
        else:
            bid_efficiency = (
                agent.total_profit /
                agent.total_spent
            )

        comparison_results.append({
            "agent": agent.name,
            "win_rate": round(win_rate, 2),
            "total_profit": agent.total_profit,
            "average_profit": round(agent.total_profit / 30, 2),
            "bid_efficiency": round(bid_efficiency, 2),
            "wins": agent.wins,
            "average_bid": round(agent.get_average_bid(), 2),
            "failed_bids": agent.failed_bids
        })

        print(
            f"{agent.name} | "
            f"Win Rate: {win_rate:.2f}% | "
            f"Total Profit: {agent.total_profit} | "
            f"Average Profit: {agent.total_profit / 30:.2f} | "
            f"Bid Efficiency: {bid_efficiency:.2f}"
        )

    os.makedirs("results", exist_ok = True)

    with open("results/comparison_metrics.json", "w") as f:
        json.dump(comparison_results, f, indent = 4)

    print("\nComparison metrics exported successfully.")

run_comparison_test()