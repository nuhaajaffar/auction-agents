import sys
import os
import csv
import statistics

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from environment.auction_environment import AuctionEnvironment
from memory import Memory

from agents.random_agent import RandomAgent
from agents.conservative_agent import ConservativeAgent
from agents.aggressive_agent import AggressiveAgent
from agents.sniper_agent import SniperAgent
from agents.adaptive_agent import AdaptiveAgent

NUM_RUNS = 10
NUM_ROUNDS = 30
STARTING_BALANCE = 1500

def ensure_result_folders():
    os.makedirs("results/raw", exist_ok = True)
    os.makedirs("results/summaries", exist_ok = True)

def run_single_simulation(agents, num_rounds = NUM_ROUNDS):

    memory = Memory()

    env = AuctionEnvironment(
        agents = agents,
        memory = memory,
        num_rounds = num_rounds
    )

    env.run_simulation()

    results = []

    for agent in agents:

        win_rate = agent.get_win_rate(num_rounds)

        if agent.total_spent == 0:
            efficiency = 0
        else:
            efficiency = agent.total_profit / agent.total_spent

        results.append({
            "agent": agent.name,
            "wins": agent.wins,
            "win_rate": win_rate,
            "total_profit": agent.total_profit,
            "average_bid": agent.get_average_bid(),
            "efficiency": efficiency,
            "failed_bids": agent.failed_bids
        })

    return results

def experiment_1_strategy_comparison():

    print("\n===== EXPERIMENT 1: STRATEGY COMPARISON =====")

    raw_results = []

    for run in range(1, NUM_RUNS + 1):

        agents = [
            RandomAgent("Random Agent", balance = STARTING_BALANCE),
            ConservativeAgent("Conservative Agent", balance = STARTING_BALANCE),
            AggressiveAgent("Aggressive Agent", balance = STARTING_BALANCE),
            SniperAgent("Sniper Agent", balance = STARTING_BALANCE),
            AdaptiveAgent("Adaptive Agent", balance = STARTING_BALANCE)
        ]

        run_results = run_single_simulation(agents)

        for row in run_results:
            row["run"] = run
            raw_results.append(row)

    save_raw_csv(
        "results/raw/experiment_1_strategy_comparison_raw.csv",
        raw_results
    )

    save_summary_csv(
        "results/summaries/experiment_1_strategy_comparison_summary.csv",
        raw_results,
        group_key = "agent"
    )

def save_raw_csv(filename, rows):

    if not rows:
        return

    with open(filename, "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved raw results: {filename}")

def save_summary_csv(filename, rows, group_key):

    grouped = {}

    for row in rows:
        key = row[group_key]

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(row)

    summary_rows = []

    for key, values in grouped.items():
        profits = [v["total_profit"] for v in values]
        win_rates = [v["win_rate"] for v in values]
        efficiencies = [v["efficiency"] for v in values]

        summary_rows.append({
            group_key: key,
            "avg_profit": round(statistics.mean(profits), 2),
            "std_profit": round(statistics.stdev(profits), 2) if len(profits) > 1 else 0,
            "avg_win_rate": round(statistics.mean(win_rates), 4),
            "std_win_rate": round(statistics.stdev(win_rates), 4) if len(win_rates) > 1 else 0,
            "avg_efficiency": round(statistics.mean(efficiencies), 4),
            "std_efficiency": round(statistics.stdev(efficiencies), 4) if len(efficiencies) > 1 else 0
        })

    with open(filename, "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved summary results: {filename}")

if __name__ == "__main__":
    ensure_result_folders()
    experiment_1_strategy_comparison()