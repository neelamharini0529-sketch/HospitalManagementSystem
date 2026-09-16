import sqlite3
from datetime import datetime

from database import get_connection


def admit_patient(patient_id, doctor_id=None, diagnosis=None):
    """
    Admit a patient and automatically allocate
    the first available room.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check if patient exists
        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nAdmission failed!")
            print("Patient does not exist.")
            return None

        # Check if doctor exists (if doctor_id is provided)
        if doctor_id is not None:
            cursor.execute("""
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = ?
            """, (doctor_id,))

            doctor = cursor.fetchone()

            if not doctor:
                print("\nAdmission failed!")
                print("Doctor does not exist.")
                return None

        # Find first available room
        cursor.execute("""
            SELECT room_id, room_number
            FROM rooms
            WHERE status = 'Available'
            ORDER BY room_id
            LIMIT 1
        """)

        room = cursor.fetchone()

        if not room:
            print("\nAdmission failed!")
            print("No rooms are currently available.")
            return None

        room_id = room[0]
        room_number = room[1]

        # Get current date
        admission_date = datetime.now().strftime("%Y-%m-%d")

        # Create admission record
        cursor.execute("""
            INSERT INTO admissions (
                patient_id,
                room_id,
                doctor_id,
                admission_date,
                diagnosis,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            room_id,
            doctor_id,
            admission_date,
            diagnosis,
            "Admitted"
        ))

        admission_id = cursor.lastrowid

        # Change room status to Occupied
        cursor.execute("""
            UPDATE rooms
            SET status = 'Occupied'
            WHERE room_id = ?
        """, (room_id,))

        connection.commit()

        print("\nPatient admitted successfully!")
        print(f"Admission ID: {admission_id}")
        print(f"Automatically allocated Room: {room_number}")

        return admission_id

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return None

    finally:
        connection.close()


def discharge_patient(admission_id):
    """Discharge a patient and make their room available again."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Find active admission
        cursor.execute("""
            SELECT room_id
            FROM admissions
            WHERE admission_id = ?
            AND status = 'Admitted'
        """, (admission_id,))

        admission = cursor.fetchone()

        if not admission:
            print("\nDischarge failed!")
            print("Active admission not found.")
            return False

        room_id = admission[0]

        discharge_date = datetime.now().strftime("%Y-%m-%d")

        # Update admission status
        cursor.execute("""
            UPDATE admissions
            SET status = 'Discharged',
                discharge_date = ?
            WHERE admission_id = ?
        """, (
            discharge_date,
            admission_id
        ))

        # Make room available again
        cursor.execute("""
            UPDATE rooms
            SET status = 'Available'
            WHERE room_id = ?
        """, (room_id,))

        connection.commit()

        print("\nPatient discharged successfully!")
        print(f"Room ID {room_id} is now available.")

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


def view_admissions():
    """Display all hospital admissions."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                admissions.admission_id,
                patients.first_name,
                patients.last_name,
                rooms.room_number,
                admissions.admission_date,
                admissions.discharge_date,
                admissions.diagnosis,
                admissions.status
            FROM admissions
            JOIN patients
                ON admissions.patient_id = patients.patient_id
            JOIN rooms
                ON admissions.room_id = rooms.room_id
            ORDER BY admissions.admission_id
        """)

        admissions = cursor.fetchall()

        if not admissions:
            print("\nNo admissions found.")
            return

        print("\n========== ADMISSION LIST ==========")

        for admission in admissions:
            print(f"\nAdmission ID: {admission[0]}")
            print(f"Patient: {admission[1]} {admission[2]}")
            print(f"Room Number: {admission[3]}")
            print(f"Admission Date: {admission[4]}")
            print(f"Discharge Date: {admission[5]}")
            print(f"Diagnosis: {admission[6]}")
            print(f"Status: {admission[7]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()