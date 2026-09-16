
import sqlite3
from datetime import datetime

from database import get_connection


# ============================================================
# SCHEDULE APPOINTMENT
# ============================================================

def schedule_appointment(
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    reason=None
):
    """
    Schedule an appointment.

    Prevents:
    - Invalid patients
    - Invalid doctors
    - Invalid date/time formats
    - Doctor double-booking
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # VALIDATE DATE
        # ----------------------------------------------------

        try:
            datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            )
        except ValueError:
            print("\nAppointment failed!")
            print("Invalid date format.")
            print("Use YYYY-MM-DD.")
            return False

        # ----------------------------------------------------
        # VALIDATE TIME
        # ----------------------------------------------------

        try:
            datetime.strptime(
                appointment_time,
                "%H:%M"
            )
        except ValueError:
            print("\nAppointment failed!")
            print("Invalid time format.")
            print("Use HH:MM.")
            return False

        # ----------------------------------------------------
        # CHECK PATIENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
            """,
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:
            print("\nAppointment failed!")
            print("Patient does not exist.")
            return False

        # ----------------------------------------------------
        # CHECK DOCTOR
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT doctor_id
            FROM doctors
            WHERE doctor_id = ?
            """,
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor is None:
            print("\nAppointment failed!")
            print("Doctor does not exist.")
            return False

        # ----------------------------------------------------
        # CHECK DOCTOR DOUBLE-BOOKING
        # ----------------------------------------------------
        #
        # Scheduled  -> blocks
        # Completed  -> blocks
        # Cancelled  -> does NOT block
        #
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                appointment_id,
                patient_id,
                status
            FROM appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND status != 'Cancelled'
            """,
            (
                doctor_id,
                appointment_date,
                appointment_time
            )
        )

        existing_appointment = cursor.fetchone()

        if existing_appointment:

            print("\nAppointment failed!")
            print(
                "Doctor is already booked "
                "at this date and time."
            )

            print(
                f"Existing Appointment ID: "
                f"{existing_appointment[0]}"
            )

            print(
                f"Existing Status: "
                f"{existing_appointment[2]}"
            )

            return False

        # ----------------------------------------------------
        # INSERT APPOINTMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO appointments (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                "Scheduled"
            )
        )

        appointment_id = cursor.lastrowid

        connection.commit()

        print("\nAppointment scheduled successfully!")
        print(f"Appointment ID: {appointment_id}")

        return True

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return False

    finally:

        connection.close()


# ============================================================
# VIEW ALL APPOINTMENTS
# ============================================================

def view_appointments():
    """Display all appointments."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                appointment_id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                status
            FROM appointments
            ORDER BY
                appointment_date,
                appointment_time
            """
        )

        appointments = cursor.fetchall()

        if not appointments:
            print("\nNo appointments found.")
            return

        print("\n")
        print("=" * 90)
        print("            ALL APPOINTMENTS")
        print("=" * 90)

        for appointment in appointments:

            print("\n--------------------------------------------")

            print(
                f"Appointment ID : {appointment[0]}"
            )

            print(
                f"Patient ID     : {appointment[1]}"
            )

            print(
                f"Doctor ID      : {appointment[2]}"
            )

            print(
                f"Date           : {appointment[3]}"
            )

            print(
                f"Time           : {appointment[4]}"
            )

            print(
                f"Reason         : {appointment[5]}"
            )

            print(
                f"Status         : {appointment[6]}"
            )

        print("\n" + "=" * 90)

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

    finally:

        connection.close()


# ============================================================
# UPDATE APPOINTMENT STATUS
# ============================================================

def update_appointment_status(
    appointment_id,
    status
):
    """
    Update appointment status.

    Valid statuses:
    Scheduled
    Completed
    Cancelled
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # CHECK APPOINTMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                appointment_id,
                status
            FROM appointments
            WHERE appointment_id = ?
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("\nAppointment does not exist.")
            return False

        # ----------------------------------------------------
        # VALIDATE STATUS
        # ----------------------------------------------------

        valid_statuses = [
            "Scheduled",
            "Completed",
            "Cancelled"
        ]

        status = status.strip().title()

        if status not in valid_statuses:

            print("\nInvalid appointment status.")

            print(
                "Valid statuses: "
                "Scheduled, Completed, Cancelled"
            )

            return False

        # ----------------------------------------------------
        # UPDATE STATUS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE appointments
            SET status = ?
            WHERE appointment_id = ?
            """,
            (
                status,
                appointment_id
            )
        )

        connection.commit()

        print(
            "\nAppointment status "
            "updated successfully!"
        )

        print(
            f"Appointment ID: {appointment_id}"
        )

        print(
            f"New Status: {status}"
        )

        return True

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return False

    finally:

        connection.close()


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

def cancel_appointment(appointment_id):
    """Cancel an appointment."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # CHECK APPOINTMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                appointment_id,
                status
            FROM appointments
            WHERE appointment_id = ?
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:

            print("\nAppointment does not exist.")

            return False

        # ----------------------------------------------------
        # CHECK IF ALREADY CANCELLED
        # ----------------------------------------------------

        if appointment[1] == "Cancelled":

            print("\nAppointment is already cancelled.")

            return False

        # ----------------------------------------------------
        # CANCEL
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE appointment_id = ?
            """,
            (appointment_id,)
        )

        connection.commit()

        print(
            "\nAppointment cancelled successfully!"
        )

        print(
            f"Appointment ID: {appointment_id}"
        )

        return True

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return False

    finally:

        connection.close()


# ============================================================
# VIEW PATIENT APPOINTMENTS
# ============================================================

def view_patient_appointments(patient_id):
    """Display appointments for one patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # CHECK PATIENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
            """,
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:

            print("\nPatient does not exist.")

            return False

        # ----------------------------------------------------
        # GET APPOINTMENTS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                appointment_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                status
            FROM appointments
            WHERE patient_id = ?
            ORDER BY
                appointment_date,
                appointment_time
            """,
            (patient_id,)
        )

        appointments = cursor.fetchall()

        if not appointments:

            print(
                "\nNo appointments found "
                "for this patient."
            )

            return False

        print("\n")
        print("=" * 70)
        print("    PATIENT APPOINTMENTS")
        print("=" * 70)

        for appointment in appointments:

            print(
                "\n--------------------------------------------"
            )

            print(
                f"Appointment ID : {appointment[0]}"
            )

            print(
                f"Doctor ID      : {appointment[1]}"
            )

            print(
                f"Date           : {appointment[2]}"
            )

            print(
                f"Time           : {appointment[3]}"
            )

            print(
                f"Reason         : {appointment[4]}"
            )

            print(
                f"Status         : {appointment[5]}"
            )

        print("\n" + "=" * 70)

        return True

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

        return False

    finally:

        connection.close()

