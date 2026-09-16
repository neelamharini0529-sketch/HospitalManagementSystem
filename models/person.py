class Person:
    """Base class for all people in the hospital system."""

    def __init__(self, first_name, last_name, gender, phone, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone = phone
        self.email = email

    def get_full_name(self):
        """Return the person's full name."""
        return f"{self.first_name} {self.last_name}"

    def display_basic_info(self):
        """Display basic information about the person."""
        print(f"Name: {self.get_full_name()}")
        print(f"Gender: {self.gender}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")