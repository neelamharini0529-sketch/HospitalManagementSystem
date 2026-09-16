class MedicalHistory:
    """Represents a patient's medical history record."""

    def __init__(
        self,
        patient_id,
        doctor_id,
        record_date,
        diagnosis=None,
        treatment=None,
        allergies=None,
        notes=None
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.record_date = record_date
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.allergies = allergies
        self.notes = notes

    def display_history(self):
        """Display medical history information."""

        print("\n--- Medical History Record ---")
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Record Date: {self.record_date}")
        print(f"Diagnosis: {self.diagnosis}")
        print(f"Treatment: {self.treatment}")
        print(f"Allergies: {self.allergies}")
        print(f"Notes: {self.notes}")


if __name__ == "__main__":
    history = MedicalHistory(
        patient_id=1,
        doctor_id=1,
        record_date="2026-08-31",
        diagnosis="Heart condition",
        treatment="Medication and monitoring",
        allergies="None",
        notes="Patient should return for follow-up"
    )

    history.display_history()