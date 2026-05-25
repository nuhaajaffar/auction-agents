# stores item value

class AuctionItem:

    def __init__(self, item_id, true_value):

        self.item_id = item_id
        self.true_value = true_value

    def __str__(self):
        
        return f"Item {self.item_id} | Value: {self.true_value}"