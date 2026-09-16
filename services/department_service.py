import sqlite3

from database import get_connection


def add_department(name, description=None):
    """Add a new department to the hospital."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO departments (name, description)
            VALUES (?, ?)
        """, (
            name,
            description
        ))

        connection.commit()

        print("\nDepartment added successfully!")
        print(f"Department ID: {cursor.lastrowid}")

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        print("\nDepartment could not be added.")
        print("A department with this name already exists.")

        return None

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

        return None

    finally:
        connection.close()


def view_departments():
    """Display all hospital departments."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT department_id, name, description
            FROM departments
            ORDER BY department_id
        """)

        departments = cursor.fetchall()

        if not departments:
            print("\nNo departments found.")
            return

        print("\n========== DEPARTMENT LIST ==========")

        for department in departments:
            print(f"\nDepartment ID: {department[0]}")
            print(f"Name: {department[1]}")
            print(f"Description: {department[2]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def search_department(department_id):
    """Search for a department using its ID."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT department_id, name, description
            FROM departments
            WHERE department_id = ?
        """, (department_id,))

        department = cursor.fetchone()

        if department:
            print("\n========== DEPARTMENT INFORMATION ==========")
            print(f"Department ID: {department[0]}")
            print(f"Name: {department[1]}")
            print(f"Description: {department[2]}")
        else:
            print("\nDepartment not found.")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()