import sqlite3

from database import get_connection


def show_dashboard():
    """Display hospital summary information."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==========================================
        # PATIENT COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patients
        """)

        total_patients = cursor.fetchone()[0]


        # ==========================================
        # DOCTOR COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM doctors
        """)

        total_doctors = cursor.fetchone()[0]


        # ==========================================
        # STAFF COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM staff
        """)

        total_staff = cursor.fetchone()[0]


        # ==========================================
        # APPOINTMENT COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM appointments
        """)

        total_appointments = cursor.fetchone()[0]


        # ==========================================
        # ADMITTED PATIENTS
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM admissions
            WHERE status = 'Admitted'
        """)

        admitted_patients = cursor.fetchone()[0]


        # ==========================================
        # MEDICINE COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
        """)

        total_medicines = cursor.fetchone()[0]


        # ==========================================
        # LOW STOCK MEDICINES
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
            WHERE stock_quantity <= reorder_level
        """)

        low_stock_medicines = cursor.fetchone()[0]


        # ==========================================
        # PENDING BILLS
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM bills
            WHERE payment_status = 'Pending'
        """)

        pending_bills = cursor.fetchone()[0]


        # ==========================================
        # TOTAL REVENUE
        # ==========================================

        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM bills
            WHERE payment_status = 'Paid'
        """)

        total_revenue = cursor.fetchone()[0]


        # ==========================================
        # DISPLAY DASHBOARD
        # ==========================================

        print("\n")
        print("================================================")
        print("          HOSPITAL DASHBOARD")
        print("================================================")

        print(f"\nTotal Patients       : {total_patients}")
        print(f"Total Doctors        : {total_doctors}")
        print(f"Total Staff          : {total_staff}")
        print(f"Total Appointments   : {total_appointments}")
        print(f"Currently Admitted   : {admitted_patients}")
        print(f"Total Medicines      : {total_medicines}")

        print("\n---------------- ALERTS ----------------")

        print(
            f"Low Stock Medicines  : {low_stock_medicines}"
        )

        print(
            f"Pending Bills        : {pending_bills}"
        )

        print("\n---------------- FINANCE ----------------")

        print(
            f"Total Paid Revenue   : ₹{total_revenue:.2f}"
        )

        print("\n================================================")

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

    finally:

        connection.close()