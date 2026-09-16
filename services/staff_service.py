import sqlite3

from database import get_connection


def add_staff(
    first_name,
    last_name,
    gender,
    phone,
    email,
    job_title,
    salary
):
    """Add a new staff member."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Validate salary
        if salary < 0:
            print("\nStaff registration failed!")
            print("Salary cannot be negative.")
            return None

        # Insert staff member
        cursor.execute("""
            INSERT INTO staff (
                first_name,
                last_name,
                gender,
                phone,
                email,
                job_title,
                salary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            gender,
            phone,
            email,
            job_title,
            salary
        ))

        staff_id = cursor.lastrowid

        connection.commit()

        print("\nStaff member added successfully!")
        print(f"Staff ID: {staff_id}")

        return staff_id

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return None

    finally:

        connection.close()


def view_staff():
    """Display all staff members."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                staff_id,
                first_name,
                last_name,
                gender,
                phone,
                email,
                job_title,
                salary
            FROM staff
            ORDER BY staff_id
        """)

        staff_members = cursor.fetchall()

        if not staff_members:
            print("\nNo staff members found.")
            return

        print("\n========== STAFF LIST ==========")

        for staff in staff_members:

            print("\n--------------------------------")
            print(f"Staff ID: {staff[0]}")
            print(f"Name: {staff[1]} {staff[2]}")
            print(f"Gender: {staff[3]}")
            print(f"Phone: {staff[4]}")
            print(f"Email: {staff[5]}")
            print(f"Job Title: {staff[6]}")
            print(f"Salary: ₹{staff[7]:.2f}")

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

    finally:

        connection.close()


def search_staff_by_job(job_title):
    """Search staff members by job title."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                staff_id,
                first_name,
                last_name,
                phone,
                email,
                job_title,
                salary
            FROM staff
            WHERE job_title LIKE ?
            ORDER BY first_name
        """, (
            "%" + job_title + "%",
        ))

        staff_members = cursor.fetchall()

        if not staff_members:

            print(
                f"\nNo staff found for job: {job_title}"
            )

            return

        print(
            f"\n========== STAFF: {job_title.upper()} =========="
        )

        for staff in staff_members:

            print("\n--------------------------------")
            print(f"Staff ID: {staff[0]}")
            print(f"Name: {staff[1]} {staff[2]}")
            print(f"Phone: {staff[3]}")
            print(f"Email: {staff[4]}")
            print(f"Job Title: {staff[5]}")
            print(f"Salary: ₹{staff[6]:.2f}")

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

    finally:

        connection.close()


def delete_staff(staff_id):
    """Delete a staff member."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT staff_id
            FROM staff
            WHERE staff_id = ?
        """, (staff_id,))

        staff = cursor.fetchone()

        if not staff:

            print("\nStaff member not found.")

            return False

        cursor.execute("""
            DELETE FROM staff
            WHERE staff_id = ?
        """, (staff_id,))

        connection.commit()

        print("\nStaff member deleted successfully!")
        print(f"Staff ID: {staff_id}")

        return True

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return False

    finally:

        connection.close()