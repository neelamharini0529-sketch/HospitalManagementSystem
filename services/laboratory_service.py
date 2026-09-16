import sqlite3
from datetime import datetime

from database import get_connection


def add_laboratory_test(
    patient_id,
    doctor_id,
    test_name,
    result=None,
    status="Pending",
    notes=None
):
    """Add a laboratory test for a patient."""

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
            print("\nLaboratory test failed!")
            print("Patient does not exist.")
            return None

        # Check whether doctor exists
        if doctor_id is not None:
            cursor.execute("""
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = ?
            """, (doctor_id,))

            doctor = cursor.fetchone()

            if not doctor:
                print("\nLaboratory test failed!")
                print("Doctor does not exist.")
                return None

        # Get today's date
        test_date = datetime.now().strftime("%Y-%m-%d")

        # Insert laboratory test
        cursor.execute("""
            INSERT INTO laboratory_tests (
                patient_id,
                doctor_id,
                test_name,
                test_date,
                result,
                status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            doctor_id,
            test_name,
            test_date,
            result,
            status,
            notes
        ))

        test_id = cursor.lastrowid

        connection.commit()

        print("\nLaboratory test added successfully!")
        print(f"Test ID: {test_id}")

        return test_id

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return None

    finally:
        connection.close()


def view_laboratory_tests():
    """Display all laboratory tests."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                laboratory_tests.test_id,
                patients.first_name,
                patients.last_name,
                doctors.first_name,
                doctors.last_name,
                laboratory_tests.test_name,
                laboratory_tests.test_date,
                laboratory_tests.result,
                laboratory_tests.status,
                laboratory_tests.notes

            FROM laboratory_tests

            JOIN patients
                ON laboratory_tests.patient_id =
                   patients.patient_id

            LEFT JOIN doctors
                ON laboratory_tests.doctor_id =
                   doctors.doctor_id

            ORDER BY laboratory_tests.test_id
        """)

        tests = cursor.fetchall()

        if not tests:
            print("\nNo laboratory tests found.")
            return

        print("\n========== LABORATORY TEST LIST ==========")

        for test in tests:

            print("\n--------------------------------")
            print(f"Test ID: {test[0]}")
            print(f"Patient: {test[1]} {test[2]}")

            if test[3]:
                print(f"Doctor: Dr. {test[3]} {test[4]}")
            else:
                print("Doctor: Not specified")

            print(f"Test Name: {test[5]}")
            print(f"Test Date: {test[6]}")
            print(f"Result: {test[7]}")
            print(f"Status: {test[8]}")
            print(f"Notes: {test[9]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def update_test_result(
    test_id,
    result,
    notes=None
):
    """Update the result of a laboratory test."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check whether test exists
        cursor.execute("""
            SELECT test_id
            FROM laboratory_tests
            WHERE test_id = ?
        """, (test_id,))

        test = cursor.fetchone()

        if not test:
            print("\nTest not found.")
            return False

        cursor.execute("""
            UPDATE laboratory_tests
            SET result = ?,
                status = 'Completed',
                notes = ?
            WHERE test_id = ?
        """, (
            result,
            notes,
            test_id
        ))

        connection.commit()

        print("\nLaboratory test result updated successfully!")
        print(f"Test ID: {test_id}")
        print("Status: Completed")

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


def view_patient_laboratory_history(patient_id):
    """Display all laboratory tests for a specific patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check patient
        cursor.execute("""
            SELECT first_name, last_name
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nPatient not found.")
            return

        # Get patient's tests
        cursor.execute("""
            SELECT
                test_id,
                test_name,
                test_date,
                result,
                status,
                notes

            FROM laboratory_tests

            WHERE patient_id = ?

            ORDER BY test_date DESC
        """, (patient_id,))

        tests = cursor.fetchall()

        print("\n========== PATIENT LABORATORY HISTORY ==========")
        print(f"Patient: {patient[0]} {patient[1]}")

        if not tests:
            print("\nNo laboratory tests found.")
            return

        for test in tests:

            print("\n--------------------------------")
            print(f"Test ID: {test[0]}")
            print(f"Test Name: {test[1]}")
            print(f"Test Date: {test[2]}")
            print(f"Result: {test[3]}")
            print(f"Status: {test[4]}")
            print(f"Notes: {test[5]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()