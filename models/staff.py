from models.person import Person


class Staff(Person):
    """Represents a staff member in the hospital."""

    def __init__(
        self,
        first_name,
        last_name,
        gender,
        phone,
        role,
        salary,
        joining_date,
        email=None
    ):
        # Call the constructor of the parent Person class
        super().__init__(
            first_name,
            last_name,
            gender,
            phone,
            email
        )

        # Staff-specific attributes
        self.role = role
        self.salary = salary
        self.joining_date = joining_date

    def display_staff_info(self):
        """Display complete staff information."""

        print("\n--- Staff Information ---")
        print(f"Name: {self.get_full_name()}")
        print(f"Gender: {self.gender}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Role: {self.role}")
        print(f"Salary: ₹{self.salary}")
        print(f"Joining Date: {self.joining_date}")


# Test the Staff class
if __name__ == "__main__":

    staff_member = Staff(
        first_name="Priya",
        last_name="Sharma",
        gender="Female",
        phone="9876543212",
        role="Nurse",
        salary=35000,
        joining_date="2026-08-31",
        email="priya.sharma@hospital.com"
    )

    staff_member.display_staff_info()
    