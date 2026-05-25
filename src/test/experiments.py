import sys
import os
import csv
import statistics
import random

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
            "agent_type": agent.__class__.__name__,
            "wins": agent.wins,
            "win_rate": win_rate,
            "total_profit": agent.total_profit,
            "average_bid": agent.get_average_bid(),
            "efficiency": efficiency,
            "failed_bids": agent.failed_bids
        })

    return results

def create_agent_set(num_agents):

    agent_classes = [
        RandomAgent,
        ConservativeAgent,
        AggressiveAgent,
        SniperAgent,
        AdaptiveAgent
    ]

    agents = []

    for i in range(num_agents):

        agent_class = agent_classes[i % len(agent_classes)]

        agent_name = f"{agent_class.__name__} {i + 1}"

        agents.append(
            agent_class(
                agent_name,
                balance = STARTING_BALANCE
            )
        )

    return agents

def create_agents():
    return [
        RandomAgent("Random Agent", balance = STARTING_BALANCE),
        ConservativeAgent("Conservative Agent", balance = STARTING_BALANCE),
        AggressiveAgent("Aggressive Agent", balance = STARTING_BALANCE),
        SniperAgent("Sniper Agent", balance = STARTING_BALANCE),
        AdaptiveAgent("Adaptive Agent", balance = STARTING_BALANCE, use_memory = True)
    ]

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

def experiment_2_number_of_agents():

    print("\n===== EXPERIMENT 2: NUMBER OF AGENTS =====")

    raw_results = []

    agent_counts = [5, 10, 20]

    for num_agents in agent_counts:

        for run in range(1, NUM_RUNS + 1):

            agents = create_agent_set(num_agents)

            run_results = run_single_simulation(agents)

            for row in run_results:
                row["run"] = run
                row["num_agents"] = num_agents
                raw_results.append(row)

    save_raw_csv(
        "results/raw/experiment_2_number_of_agents_raw.csv",
        raw_results
    )

    save_summary_csv(
        "results/summaries/experiment_2_number_of_agents_summary.csv",
        raw_results,
        group_key = "num_agents"
    )

    save_grouped_summary_csv(
        "results/summaries/experiment_2_number_of_agents_by_type_summary.csv",
        raw_results,
        group_keys = ["num_agents", "agent_type"]
    )

def experiment_3_information_availability():

    print("\n===== EXPERIMENT 3: INFORMATION AVAILABILITY =====")

    raw_results = []
    adaptive_only_results = []

    memory_conditions = [
        ("yes", True),
        ("no", False)
    ]

    for run in range(1, NUM_RUNS + 1):

        for memory_label, memory_access in memory_conditions:

            # same seed for both memory/no-memory condition to ensure fairness
            random.seed(3000 + run)

            agents = [
                RandomAgent("Random Agent", balance = STARTING_BALANCE),
                ConservativeAgent("Conservative Agent", balance = STARTING_BALANCE),
                AggressiveAgent("Aggressive Agent", balance = STARTING_BALANCE),
                SniperAgent("Sniper Agent", balance = STARTING_BALANCE),
                AdaptiveAgent(
                    "Adaptive Agent",
                    balance = STARTING_BALANCE,
                    use_memory = memory_access
                )
            ]

            run_results = run_single_simulation(agents)

            for row in run_results:
                row["run"] = run
                row["memory_access"] = memory_label
                raw_results.append(row)

                if row["agent_type"] == "AdaptiveAgent":
                    adaptive_only_results.append(row)

    save_raw_csv(
        "results/raw/experiment_3_information_availability_raw.csv",
        raw_results
    )

    save_summary_csv(
        "results/summaries/experiment_3_information_availability_adaptive_summary.csv",
        adaptive_only_results,
        group_key = "memory_access"
    )

    save_grouped_summary_csv(
        "results/summaries/experiment_3_information_availability_by_type_summary.csv",
        raw_results,
        group_keys = ["memory_access", "agent_type"]
    )

def experiment_4_market_noise():

    print("\n===== EXPERIMENT 4: MARKET NOISE =====")

    noise_levels = ["low", "medium", "high"]

    raw_results = []

    for noise_level in noise_levels:

        for run in range(1, NUM_RUNS + 1):

            # same seed pattern for fair comparison across noise levels
            random.seed(4000 + run)

            agents = create_agents()
            memory = Memory()

            env = AuctionEnvironment(
                agents = agents,
                memory = memory,
                num_rounds = NUM_ROUNDS,
                noise_level = noise_level
            )

            env.run_simulation()

            for agent in agents:

                if agent.total_spent == 0:
                    efficiency = 0
                else:
                    efficiency = agent.total_profit / agent.total_spent

                raw_results.append({
                    "agent": agent.name,
                    "agent_type": agent.__class__.__name__,
                    "wins": agent.wins,
                    "win_rate": agent.get_win_rate(NUM_ROUNDS),
                    "total_profit": agent.total_profit,
                    "average_bid": agent.get_average_bid(),
                    "efficiency": efficiency,
                    "failed_bids": agent.failed_bids,
                    "run": run,
                    "noise_level": noise_level
                })

    save_raw_csv(
        "results/raw/experiment_4_market_noise_raw.csv",
        raw_results
    )

    save_summary_csv(
        "results/summaries/experiment_4_market_noise_summary.csv",
        raw_results,
        group_key = "noise_level"
    )

    save_grouped_summary_csv(
        "results/summaries/experiment_4_market_noise_by_type_summary.csv",
        raw_results,
        group_keys = ["noise_level", "agent_type"]
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

def save_grouped_summary_csv(filename, rows, group_keys):

    grouped = {}

    for row in rows:
        key = tuple(row[group_key] for group_key in group_keys)

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(row)

    summary_rows = []

    for key, values in grouped.items():
        profits = [v["total_profit"] for v in values]
        win_rates = [v["win_rate"] for v in values]
        efficiencies = [v["efficiency"] for v in values]

        summary_row = {}

        for i, group_key in enumerate(group_keys):
            summary_row[group_key] = key[i]

        summary_row.update({
            "avg_profit": round(statistics.mean(profits), 2),
            "std_profit": round(statistics.stdev(profits), 2) if len(profits) > 1 else 0,
            "avg_win_rate": round(statistics.mean(win_rates), 4),
            "std_win_rate": round(statistics.stdev(win_rates), 4) if len(win_rates) > 1 else 0,
            "avg_efficiency": round(statistics.mean(efficiencies), 4),
            "std_efficiency": round(statistics.stdev(efficiencies), 4) if len(efficiencies) > 1 else 0
        })

        summary_rows.append(summary_row)

    with open(filename, "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved grouped summary results: {filename}")

if __name__ == "__main__":
    ensure_result_folders()
    # experiment_1_strategy_comparison()
    # experiment_2_number_of_agents()
    # experiment_3_information_availability()
    experiment_4_market_noise()