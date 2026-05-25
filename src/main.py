from agents.random_agent import RandomAgent
from agents.conservative_agent import ConservativeAgent
from agents.aggressive_agent import AggressiveAgent
from agents.sniper_agent import SniperAgent

from environment.auction_environment import AuctionEnvironment

agents = [
    RandomAgent("Agent A"),
    RandomAgent("Agent B"),
    RandomAgent("Agent C"),
    RandomAgent("Random"),
    ConservativeAgent("Conservative"),
    AggressiveAgent("Aggressive"),
    SniperAgent("Sniper")
]

environment = AuctionEnvironment(
    agents = agents,
    num_rounds = 20
)

environment.run_simulation()