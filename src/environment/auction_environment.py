# create items
# ask agents for bids
# determine winner
# calculate profit
# store results

import random
import json
import os

from environment.item import AuctionItem

class AuctionEnvironment:

    def __init__(self, agents, memory, num_rounds = 100):

        self.agents = agents
        self.memory = memory
        self.num_rounds = num_rounds

        self.results = []

    def generate_item(self, round_number):

        value = random.randint(50, 200)

        return AuctionItem(round_number, value)

    def collect_bids(self, item, current_round, current_highest_bid = 0):

        bids = {}

        for agent in self.agents:

            bid = agent.place_bid(item, current_highest_bid, current_round, self.num_rounds, self.memory)

            bids[agent] = bid

            if bid > current_highest_bid:
                current_highest_bid = bid

        return bids

    def determine_winner(self, bids):

        # remove invalid/non-participating bids
        valid_bids = {
            agent: bid
            for agent, bid in bids.items()
            if bid > 0
        }

        # no valid bids
        if not valid_bids:
            return None, 0

        highest_bid = max(valid_bids.values())
        highest_bidders = [
            agent for agent, bid in valid_bids.items()
            if bid == highest_bid
        ]

        winner = random.choice(highest_bidders)

        return winner, highest_bid

    def calculate_profit(self, item_value, winning_bid):

        return item_value - winning_bid

    def run_round(self, round_number):

        item = self.generate_item(round_number)

        bids = self.collect_bids(item, round_number)
        
        winner, winning_bid = self.determine_winner(bids)

        for agent, bid in bids.items():
            if winner is not None and agent != winner and bid > 0:
                self.memory.update_loss(
                    bid = bid,
                    price = item.true_value,
                    round_id = round_number
                )

        # no winner case
        if winner is None:
            print("\n====================")
            print(f"Round {round_number}")
            print(item)

            for agent, bid in bids.items():
                print(f"{agent.name} bid: {bid}")

            print("No valid bids.")

            return

        profit = self.calculate_profit(
            item.true_value,
            winning_bid
        )

        # update winner statistics
        winner.record_win()
        winner.total_spent += winning_bid
        winner.balance -= winning_bid
        winner.update_profit(profit)

        self.memory.update_win(
            bid = winning_bid,
            price = item.true_value,
            round_id = round_number
        )

        # store results
        round_result = {
            "round": round_number,
            "item_value": item.true_value,
            "winner": winner.name,
            "winning_bid": winning_bid,
            "profit": profit,
            "bids": {
                agent.name: bid
                for agent, bid in bids.items()
            }        
        }

        self.results.append(round_result)

        # console output
        print("\n====================")
        print(f"Round {round_number}")
        print(item)

        for agent, bid in bids.items():
            print(f"{agent.name} bid: {bid}")

        print(f"Winner: {winner.name}")
        print(f"Winning Bid: {winning_bid}")
        print(f"Profit: {profit}")

    def export_results(self):

        os.makedirs("results", exist_ok = True)

        with open("results/auction_history.json", "w") as f:
            json.dump(self.results, f, indent = 4)

        print("\nResults exported successfully.")

    def run_simulation(self):

        for round_number in range(1, self.num_rounds + 1):

            self.run_round(round_number)

        print("\n====================")
        print("Simulation Complete")

        print("\nFINAL SUMMARY")

        for agent in self.agents:

            print(
                f"{agent.name} | "
                f"Wins: {agent.wins} | "
                f"Total Profit: {agent.total_profit} | "
                f"Total Spent: {agent.total_spent} | "
                f"Average Bid: {agent.get_average_bid():.2f} | "
                f"Failed Bids: {agent.failed_bids}"
            )

        self.export_results()