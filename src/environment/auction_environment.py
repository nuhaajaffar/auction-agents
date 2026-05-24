# create items
# ask agents for bids
# determine winner
# calculate profit
# store results

import random

from environment.item import AuctionItem

class AuctionEnvironment:

    def __init__(self, agents, num_rounds = 100):

        self.agents = agents
        self.num_rounds = num_rounds

        self.results = []

    def generate_item(self, round_number):

        value = random.randint(50, 200)

        return AuctionItem(round_number, value)

    def collect_bids(self, item):

        bids = {}

        for agent in self.agents:

            bid = agent.place_bid(item)

            bids[agent] = bid

        return bids

    def determine_winner(self, bids):

        highest_bid = max(bids.values())

        highest_bidders = [
            agent for agent, bid in bids.items()
            if bid == highest_bid
        ]

        winner = random.choice(highest_bidders)

        return winner, highest_bid

    def calculate_profit(self, item_value, winning_bid):

        return item_value - winning_bid

    def run_round(self, round_number):

        item = self.generate_item(round_number)

        bids = self.collect_bids(item)

        winner, winning_bid = self.determine_winner(bids)

        profit = self.calculate_profit(
            item.true_value,
            winning_bid
        )

        winner.record_win()
        winner.update_profit(profit)

        round_result = {
            "round": round_number,
            "item_value": item.true_value,
            "winner": winner.name,
            "winning_bid": winning_bid,
            "profit": profit
        }

        self.results.append({
            "round": round_number,
            "item_value": item.true_value,
            "winner": winner.name,
            "winning_bid": winning_bid,
            "profit": profit,
            "bids": {agent.name: bid for agent, bid in bids.items()}
        })

        print("\n====================")
        print(f"Round {round_number}")
        print(item)

        for agent, bid in bids.items():
            print(f"{agent.name} bid: {bid}")

        print(f"Winner: {winner.name}")
        print(f"Winning Bid: {winning_bid}")
        print(f"Profit: {profit}")

        print("\nFINAL SUMMARY")

        for agent in self.agents:
            print(
                f"{agent.name} | "
                f"Wins: {agent.wins} | "
                f"Profit: {agent.total_profit}"
            )

    def run_simulation(self):

        for round_number in range(1, self.num_rounds + 1):

            self.run_round(round_number)

        print("\n====================")
        print("Simulation Complete")

        for agent in self.agents:

            print(
                f"{agent.name} | "
                f"Wins: {agent.wins} | "
                f"Total Profit: {agent.total_profit}"
            )