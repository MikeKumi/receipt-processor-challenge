class Receipt:
    """
    Receipt object used to store fields from the JSON
    Ordinarily I would turn this into an ORM. However, we are using in-memory data so I will keep it simple.
    """
    def __init__(self, json_dict):
        self.retailer = json_dict["retailer"]
        self.purchase_date = json_dict["purchaseDate"]
        self.purchase_time = json_dict["purchaseTime"]
        self.total = float(json_dict["total"])
        self.items = []
        self._build_items(json_dict["items"])

    def _build_items(self, items):
        for item in items:
            short_description = item["shortDescription"]
            price = float(item["price"])
            self.items.append(Item(short_description, price))

class Item:
    """
    Item object used to store fields from individual items from the receipt.
    """
    def __init__(self, short_description, price):
        self.short_description = short_description
        self.price = price
