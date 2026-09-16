from models.person import Person


class Doctor(Person):
    """Represents a doctor in the hospital."""

    def __init__(
        self,
        first_name,
        last_name,
        gender,
        phone,
        specialization,
        department_id,
        consultation_fee,
        email=None
    ):
        # Call the constructor of the Person class
        super().__init__(
            first_name,
            last_name,
            gender,
            phone,
            email
        )

        # Doctor-specific attributes
        self.specialization = specialization
        self.department_id = department_id
        self.consultation_fee = consultation_fee

    def display_doctor_info(self):
        """Display complete doctor information."""

        print("\n--- Doctor Information ---")
        print(f"Name: Dr. {self.get_full_name()}")
        print(f"Gender: {self.gender}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Specialization: {self.specialization}")
        print(f"Department ID: {self.department_id}")
        print(f"Consultation Fee: ₹{self.consultation_fee}")


# Test the Doctor class
if __name__ == "__main__":

    doctor = Doctor(
        first_name="Rajesh",
        last_name="Kumar",
        gender="Male",
        phone="9876543210",
        specialization="Cardiologist",
        department_id=1,
        consultation_fee=800,
        email="rajesh.kumar@hospital.com"
    )

    doctor.display_doctor_info()