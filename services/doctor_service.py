import sqlite3

from database import get_connection


def add_doctor(
    first_name,
    last_name,
    gender,
    phone,
    specialization,
    department_id,
    consultation_fee,
    email=None
):
    """Add a new doctor to the database."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check if the department exists
        cursor.execute("""
            SELECT department_id
            FROM departments
            WHERE department_id = ?
        """, (department_id,))

        department = cursor.fetchone()

        if not department:
            print("\nDoctor could not be added.")
            print("Department ID does not exist.")
            return None

        # Add doctor
        cursor.execute("""
            INSERT INTO doctors (
                first_name,
                last_name,
                gender,
                phone,
                email,
                specialization,
                department_id,
                consultation_fee
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            gender,
            phone,
            email,
            specialization,
            department_id,
            consultation_fee
        ))

        connection.commit()

        print("\nDoctor added successfully!")
        print(f"Doctor ID: {cursor.lastrowid}")

        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        print("\nDoctor could not be added.")
        print("Error:", error)
        return None

    except sqlite3.Error as error:
        print("\nDatabase error:", error)
        return None

    finally:
        connection.close()


def view_doctors():
    """Display all doctors."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                doctors.doctor_id,
                doctors.first_name,
                doctors.last_name,
                doctors.gender,
                doctors.phone,
                doctors.email,
                doctors.specialization,
                departments.name,
                doctors.consultation_fee
            FROM doctors
            LEFT JOIN departments
            ON doctors.department_id = departments.department_id
            ORDER BY doctors.doctor_id
        """)

        doctors = cursor.fetchall()

        if not doctors:
            print("\nNo doctors found.")
            return

        print("\n========== DOCTOR LIST ==========")

        for doctor in doctors:
            print(f"\nDoctor ID: {doctor[0]}")
            print(f"Name: Dr. {doctor[1]} {doctor[2]}")
            print(f"Gender: {doctor[3]}")
            print(f"Phone: {doctor[4]}")
            print(f"Email: {doctor[5]}")
            print(f"Specialization: {doctor[6]}")
            print(f"Department: {doctor[7]}")
            print(f"Consultation Fee: ₹{doctor[8]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def search_doctor(doctor_id):
    """Search for a doctor using doctor ID."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                doctors.doctor_id,
                doctors.first_name,
                doctors.last_name,
                doctors.gender,
                doctors.phone,
                doctors.email,
                doctors.specialization,
                departments.name,
                doctors.consultation_fee
            FROM doctors
            LEFT JOIN departments
            ON doctors.department_id = departments.department_id
            WHERE doctors.doctor_id = ?
        """, (doctor_id,))

        doctor = cursor.fetchone()

        if doctor:
            print("\n========== DOCTOR INFORMATION ==========")
            print(f"Doctor ID: {doctor[0]}")
            print(f"Name: Dr. {doctor[1]} {doctor[2]}")
            print(f"Gender: {doctor[3]}")
            print(f"Phone: {doctor[4]}")
            print(f"Email: {doctor[5]}")
            print(f"Specialization: {doctor[6]}")
            print(f"Department: {doctor[7]}")
            print(f"Consultation Fee: ₹{doctor[8]}")
        else:
            print("\nDoctor not found.")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()