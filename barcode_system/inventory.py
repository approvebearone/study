class Inventory:
    def __init__(self):
        self.stock = {}

    def add(self, barcode: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.stock[barcode] = self.stock.get(barcode, 0) + quantity

    def remove(self, barcode: str, quantity: int) -> None:
        if barcode not in self.stock:
            raise ValueError("Barcode not found")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.stock[barcode] < quantity:
            raise ValueError("Not enough stock to remove")
        self.stock[barcode] -= quantity

    def get_quantity(self, barcode: str) -> int:
        return self.stock.get(barcode, 0)

    def all_items(self) -> dict:
        return dict(self.stock)
