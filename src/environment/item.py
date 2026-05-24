from agents.random_agent import RandomAgent
from environment.auction_environment import AuctionEnvironment

agents = [
    RandomAgent("Agent A"),
    RandomAgent("Agent B"),
    RandomAgent("Agent C")
]

environment = AuctionEnvironment(
    agents = agents,
    num_rounds = 5
)

environment.run_simulation()