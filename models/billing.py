class Bill:
    """Represents a hospital bill."""

    def __init__(
        self,
        patient_id,
        consultation_fee=0,
        room_charge=0,
        laboratory_charge=0,
        medicine_charge=0,
        discount=0,
        tax_rate=0
    ):
        self.patient_id = patient_id
        self.consultation_fee = consultation_fee
        self.room_charge = room_charge
        self.laboratory_charge = laboratory_charge
        self.medicine_charge = medicine_charge
        self.discount = discount
        self.tax_rate = tax_rate

    def calculate_subtotal(self):
        """Calculate total before discount and tax."""

        return (
            self.consultation_fee
            + self.room_charge
            + self.laboratory_charge
            + self.medicine_charge
        )

    def calculate_discount_amount(self):
        """Calculate discount amount."""

        subtotal = self.calculate_subtotal()

        return subtotal * (self.discount / 100)

    def calculate_tax_amount(self):
        """Calculate tax after discount."""

        subtotal = self.calculate_subtotal()

        discount_amount = self.calculate_discount_amount()

        taxable_amount = subtotal - discount_amount

        return taxable_amount * (self.tax_rate / 100)

    def calculate_total(self):
        """Calculate final bill amount."""

        subtotal = self.calculate_subtotal()

        discount_amount = self.calculate_discount_amount()

        tax_amount = self.calculate_tax_amount()

        return subtotal - discount_amount + tax_amount

    def display_bill(self):
        """Display complete bill information."""

        subtotal = self.calculate_subtotal()
        discount_amount = self.calculate_discount_amount()
        tax_amount = self.calculate_tax_amount()
        total = self.calculate_total()

        print("\n========== HOSPITAL BILL ==========")

        print(f"Patient ID: {self.patient_id}")

        print("\n--- Charges ---")
        print(f"Consultation Fee: ₹{self.consultation_fee:.2f}")
        print(f"Room Charge: ₹{self.room_charge:.2f}")
        print(f"Laboratory Charge: ₹{self.laboratory_charge:.2f}")
        print(f"Medicine Charge: ₹{self.medicine_charge:.2f}")

        print(f"\nSubtotal: ₹{subtotal:.2f}")

        print(
            f"Discount ({self.discount}%): "
            f"₹{discount_amount:.2f}"
        )

        print(
            f"Tax ({self.tax_rate}%): "
            f"₹{tax_amount:.2f}"
        )

        print(f"\nFINAL BILL: ₹{total:.2f}")


if __name__ == "__main__":

    bill = Bill(
        patient_id=1,
        consultation_fee=800,
        room_charge=3000,
        laboratory_charge=1000,
        medicine_charge=500,
        discount=10,
        tax_rate=5
    )

    bill.display_bill()