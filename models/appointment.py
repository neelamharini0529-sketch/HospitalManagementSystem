class Appointment:
    """Represents a patient appointment with a doctor."""

    def __init__(
        self,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason=None,
        status="Scheduled"
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status

    def display_appointment_info(self):
        """Display appointment information."""

        print("\n--- Appointment Information ---")
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Appointment Date: {self.appointment_date}")
        print(f"Appointment Time: {self.appointment_time}")
        print(f"Reason: {self.reason}")
        print(f"Status: {self.status}")


# Test the Appointment class
if __name__ == "__main__":

    appointment = Appointment(
        patient_id=1,
        doctor_id=1,
        appointment_date="2026-09-01",
        appointment_time="10:00 AM",
        reason="Regular health checkup"
    )

    appointment.display_appointment_info()