class Medicine:
    """Represents a medicine in the hospital pharmacy."""

    def __init__(
        self,
        name,
        manufacturer,
        price,
        stock_quantity,
        expiry_date,
        reorder_level=10
    ):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price
        self.stock_quantity = stock_quantity
        self.expiry_date = expiry_date
        self.reorder_level = reorder_level

    def display_medicine_info(self):
        """Display medicine information."""

        print("\n--- Medicine Information ---")
        print(f"Name: {self.name}")
        print(f"Manufacturer: {self.manufacturer}")
        print(f"Price: ₹{self.price}")
        print(f"Stock Quantity: {self.stock_quantity}")
        print(f"Expiry Date: {self.expiry_date}")
        print(f"Reorder Level: {self.reorder_level}")


if __name__ == "__main__":

    medicine = Medicine(
        name="Paracetamol",
        manufacturer="ABC Pharma",
        price=25,
        stock_quantity=100,
        expiry_date="2027-12-31",
        reorder_level=20
    )

    medicine.display_medicine_info()