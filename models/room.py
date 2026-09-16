class Room:
    """Represents a hospital room."""

    def __init__(
        self,
        room_number,
        room_type,
        daily_charge,
        status="Available"
    ):
        self.room_number = room_number
        self.room_type = room_type
        self.daily_charge = daily_charge
        self.status = status

    def display_room_info(self):
        """Display room information."""

        print("\n--- Room Information ---")
        print(f"Room Number: {self.room_number}")
        print(f"Room Type: {self.room_type}")
        print(f"Daily Charge: ₹{self.daily_charge}")
        print(f"Status: {self.status}")


# Test the Room class
if __name__ == "__main__":

    room = Room(
        room_number="101",
        room_type="General",
        daily_charge=1500
    )

    room.display_room_info()