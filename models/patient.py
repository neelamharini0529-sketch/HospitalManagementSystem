from models.person import Person


class Patient(Person):
    """Represents a patient in the hospital."""

    def __init__(
        self,
        first_name,
        last_name,
        gender,
        phone,
        date_of_birth,
        email=None,
        address=None,
        blood_group=None,
        emergency_contact=None
    ):
        # Call the constructor of the parent Person class
        super().__init__(
            first_name,
            last_name,
            gender,
            phone,
            email
        )

        # Patient-specific attributes
        self.date_of_birth = date_of_birth
        self.address = address
        self.blood_group = blood_group
        self.emergency_contact = emergency_contact

    def display_patient_info(self):
        """Display complete patient information."""

        print("\n--- Patient Information ---")
        print(f"Name: {self.get_full_name()}")
        print(f"Gender: {self.gender}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Address: {self.address}")
        print(f"Blood Group: {self.blood_group}")
        print(f"Emergency Contact: {self.emergency_contact}")


# Test the Patient class
if __name__ == "__main__":

    patient = Patient(
        first_name="John",
        last_name="Smith",
        gender="Male",
        phone="9876543210",
        date_of_birth="1995-05-10",
        email="john@example.com",
        address="Bangalore",
        blood_group="O+",
        emergency_contact="9876543211"
    )

    patient.display_patient_info()