# stores item value

import random

class AuctionItem:

    def __init__(self, item_id, true_value):

        self.item_id = item_id
        self.true_value = true_value
        self.perceived_value = true_value

    def __str__(self):

        return (
            f"Item {self.item_id} | "
            f"True Value: {self.true_value} | "
            f"Perceived Value: {self.perceived_value}"
        )

    def apply_market_noise(self, noise_level):
        noise_ranges = {
            "low": 0.05,
            "medium": 0.15,
            "high": 0.30
        }

        noise_range = noise_ranges[noise_level]
        noise = random.uniform(-noise_range, noise_range)

        self.perceived_value = max(1, int(self.true_value * (1 + noise)))

        return self