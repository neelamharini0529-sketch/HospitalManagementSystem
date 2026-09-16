import sqlite3
from datetime import datetime

from database import get_connection


def add_medical_history(
    patient_id,
    doctor_id,
    diagnosis,
    treatment,
    allergies=None,
    notes=None
):
    """Add a medical history record for a patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==========================================
        # CHECK PATIENT
        # ==========================================

        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nMedical history failed!")
            print("Patient does not exist.")
            return None


        # ==========================================
        # CHECK DOCTOR
        # ==========================================

        if doctor_id is not None:

            cursor.execute("""
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = ?
            """, (doctor_id,))

            doctor = cursor.fetchone()

            if not doctor:
                print("\nMedical history failed!")
                print("Doctor does not exist.")
                return None


        # ==========================================
        # VALIDATE DIAGNOSIS
        # ==========================================

        if not diagnosis or not diagnosis.strip():

            print("\nMedical history failed!")
            print("Diagnosis cannot be empty.")
            return None


        # ==========================================
        # CURRENT DATE
        # ==========================================

        record_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


        # ==========================================
        # INSERT RECORD
        # ==========================================

        cursor.execute("""
            INSERT INTO medical_history (
                patient_id,
                doctor_id,
                record_date,
                diagnosis,
                treatment,
                allergies,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            doctor_id,
            record_date,
            diagnosis,
            treatment,
            allergies,
            notes
        ))


        history_id = cursor.lastrowid

        connection.commit()


        print("\nMedical history added successfully!")
        print(f"History ID: {history_id}")

        return history_id


    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return None


    finally:

        connection.close()


def view_medical_history():
    """Display all medical history records."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                medical_history.history_id,
                patients.first_name,
                patients.last_name,
                doctors.first_name,
                doctors.last_name,
                medical_history.record_date,
                medical_history.diagnosis,
                medical_history.treatment,
                medical_history.allergies,
                medical_history.notes

            FROM medical_history

            JOIN patients
                ON medical_history.patient_id =
                   patients.patient_id

            LEFT JOIN doctors
                ON medical_history.doctor_id =
                   doctors.doctor_id

            ORDER BY medical_history.record_date DESC
        """)

        records = cursor.fetchall()


        if not records:

            print("\nNo medical history records found.")

            return


        print("\n========== MEDICAL HISTORY ==========")


        for record in records:

            print("\n--------------------------------")
            print(f"History ID: {record[0]}")
            print(f"Patient: {record[1]} {record[2]}")

            if record[3]:

                print(
                    f"Doctor: Dr. "
                    f"{record[3]} {record[4]}"
                )

            else:

                print("Doctor: Not specified")

            print(f"Date: {record[5]}")
            print(f"Diagnosis: {record[6]}")
            print(f"Treatment: {record[7]}")
            print(f"Allergies: {record[8]}")
            print(f"Notes: {record[9]}")


    except sqlite3.Error as error:

        print("\nDatabase error:", error)


    finally:

        connection.close()


def view_patient_medical_history(patient_id):
    """Display medical history for one patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==========================================
        # CHECK PATIENT
        # ==========================================

        cursor.execute("""
            SELECT
                first_name,
                last_name
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()


        if not patient:

            print("\nPatient not found.")

            return


        # ==========================================
        # GET HISTORY
        # ==========================================

        cursor.execute("""
            SELECT
                medical_history.history_id,
                doctors.first_name,
                doctors.last_name,
                medical_history.record_date,
                medical_history.diagnosis,
                medical_history.treatment,
                medical_history.allergies,
                medical_history.notes

            FROM medical_history

            LEFT JOIN doctors
                ON medical_history.doctor_id =
                   doctors.doctor_id

            WHERE medical_history.patient_id = ?

            ORDER BY medical_history.record_date DESC
        """, (patient_id,))

        records = cursor.fetchall()


        print(
            "\n========== PATIENT MEDICAL HISTORY =========="
        )

        print(
            f"Patient: {patient[0]} {patient[1]}"
        )


        if not records:

            print("\nNo medical history found.")

            return


        for record in records:

            print("\n--------------------------------")

            print(
                f"History ID: {record[0]}"
            )

            if record[1]:

                print(
                    f"Doctor: Dr. "
                    f"{record[1]} {record[2]}"
                )

            print(
                f"Date: {record[3]}"
            )

            print(
                f"Diagnosis: {record[4]}"
            )

            print(
                f"Treatment: {record[5]}"
            )

            print(
                f"Allergies: {record[6]}"
            )

            print(
                f"Notes: {record[7]}"
            )


    except sqlite3.Error as error:

        print("\nDatabase error:", error)


    finally:

        connection.close()