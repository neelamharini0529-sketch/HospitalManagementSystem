class LaboratoryTest:
    """Represents a laboratory test for a patient."""

    def __init__(
        self,
        patient_id,
        doctor_id,
        test_name,
        test_date,
        result=None,
        status="Pending",
        notes=None
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.test_name = test_name
        self.test_date = test_date
        self.result = result
        self.status = status
        self.notes = notes

    def display_test_info(self):
        """Display laboratory test information."""

        print("\n--- Laboratory Test ---")
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Test Name: {self.test_name}")
        print(f"Test Date: {self.test_date}")
        print(f"Result: {self.result}")
        print(f"Status: {self.status}")
        print(f"Notes: {self.notes}")


if __name__ == "__main__":

    test = LaboratoryTest(
        patient_id=1,
        doctor_id=1,
        test_name="Blood Test",
        test_date="2026-08-31",
        result="Normal",
        status="Completed",
        notes="No abnormality detected"
    )

    test.display_test_info()