import sqlite3
from datetime import datetime

from database import get_connection


def register_patient(
    first_name,
    last_name,
    gender,
    date_of_birth,
    phone,
    email=None,
    address=None,
    blood_group=None,
    emergency_contact=None
):
    """Register a new patient in the database."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        registration_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO patients (
                first_name,
                last_name,
                gender,
                date_of_birth,
                phone,
                email,
                address,
                blood_group,
                emergency_contact,
                registration_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            gender,
            date_of_birth,
            phone,
            email,
            address,
            blood_group,
            emergency_contact,
            registration_date
        ))

        connection.commit()

        print("\nPatient registered successfully!")
        print(f"Patient ID: {cursor.lastrowid}")

        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        print("\nPatient registration failed!")
        print("Error:", error)
        return None

    except sqlite3.Error as error:
        print("\nDatabase error:", error)
        return None

    finally:
        connection.close()


def view_patients():
    """Display all registered patients."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                date_of_birth,
                phone,
                email,
                blood_group,
                registration_date
            FROM patients
            ORDER BY patient_id
        """)

        patients = cursor.fetchall()

        if not patients:
            print("\nNo patients found.")
            return

        print("\n========== PATIENT LIST ==========")

        for patient in patients:
            print(f"\nPatient ID: {patient[0]}")
            print(f"Name: {patient[1]} {patient[2]}")
            print(f"Gender: {patient[3]}")
            print(f"Date of Birth: {patient[4]}")
            print(f"Phone: {patient[5]}")
            print(f"Email: {patient[6]}")
            print(f"Blood Group: {patient[7]}")
            print(f"Registration Date: {patient[8]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def search_patient(patient_id):
    """Search for a patient using the patient ID."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                date_of_birth,
                phone,
                email,
                address,
                blood_group,
                emergency_contact,
                registration_date
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if patient:
            print("\n========== PATIENT INFORMATION ==========")
            print(f"Patient ID: {patient[0]}")
            print(f"Name: {patient[1]} {patient[2]}")
            print(f"Gender: {patient[3]}")
            print(f"Date of Birth: {patient[4]}")
            print(f"Phone: {patient[5]}")
            print(f"Email: {patient[6]}")
            print(f"Address: {patient[7]}")
            print(f"Blood Group: {patient[8]}")
            print(f"Emergency Contact: {patient[9]}")
            print(f"Registration Date: {patient[10]}")
        else:
            print("\nPatient not found.")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def update_patient(
    patient_id,
    phone=None,
    email=None,
    address=None,
    blood_group=None,
    emergency_contact=None
):
    """Update contact and other basic details of a patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check whether patient exists
        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nPatient not found.")
            return False

        cursor.execute("""
            UPDATE patients
            SET
                phone = ?,
                email = ?,
                address = ?,
                blood_group = ?,
                emergency_contact = ?
            WHERE patient_id = ?
        """, (
            phone,
            email,
            address,
            blood_group,
            emergency_contact,
            patient_id
        ))

        connection.commit()

        print("\nPatient details updated successfully!")
        return True

    except sqlite3.Error as error:

        print("\nDatabase error:", error)
        return False

    finally:

        connection.close()

def delete_patient(patient_id):
    """Delete a patient from the database."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nPatient not found.")
            return False

        cursor.execute("""
            DELETE FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        connection.commit()

        print("\nPatient deleted successfully!")
        return True

    except sqlite3.IntegrityError:
        print("\nCannot delete this patient.")
        print("The patient may have related medical records,")
        print("appointments, laboratory tests, bills, or admissions.")
        return False

    except sqlite3.Error as error:
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()