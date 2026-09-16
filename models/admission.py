class Admission:
    """Represents a patient's hospital admission."""

    def __init__(
        self,
        patient_id,
        room_id,
        admission_date,
        doctor_id=None,
        diagnosis=None,
        status="Admitted"
    ):
        self.patient_id = patient_id
        self.room_id = room_id
        self.doctor_id = doctor_id
        self.admission_date = admission_date
        self.diagnosis = diagnosis
        self.status = status

    def display_admission_info(self):
        """Display admission information."""

        print("\n--- Admission Information ---")
        print(f"Patient ID: {self.patient_id}")
        print(f"Room ID: {self.room_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Admission Date: {self.admission_date}")
        print(f"Diagnosis: {self.diagnosis}")
        print(f"Status: {self.status}")


# Test the Admission class
if __name__ == "__main__":

    admission = Admission(
        patient_id=1,
        room_id=1,
        doctor_id=1,
        admission_date="2026-08-31",
        diagnosis="Heart condition"
    )

    admission.display_admission_info()