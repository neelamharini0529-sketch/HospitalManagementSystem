import sqlite3
from datetime import datetime

from database import get_connection


def create_bill(
    patient_id,
    consultation_fee=0,
    room_charge=0,
    laboratory_charge=0,
    medicine_charge=0,
    discount=0,
    tax_rate=0
):
    """Create and save a hospital bill."""

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
            print("\nBill creation failed!")
            print("Patient does not exist.")
            return None


        # ==========================================
        # VALIDATE VALUES
        # ==========================================

        if (
            consultation_fee < 0
            or room_charge < 0
            or laboratory_charge < 0
            or medicine_charge < 0
        ):
            print("\nBill creation failed!")
            print("Charges cannot be negative.")
            return None

        if discount < 0 or discount > 100:
            print("\nBill creation failed!")
            print("Discount must be between 0 and 100.")
            return None

        if tax_rate < 0:
            print("\nBill creation failed!")
            print("Tax rate cannot be negative.")
            return None


        # ==========================================
        # CALCULATE SUBTOTAL
        # ==========================================

        subtotal = (
            consultation_fee
            + room_charge
            + laboratory_charge
            + medicine_charge
        )


        # ==========================================
        # CALCULATE DISCOUNT
        # ==========================================

        discount_amount = (
            subtotal * discount / 100
        )


        # ==========================================
        # CALCULATE TAX
        # ==========================================

        taxable_amount = (
            subtotal - discount_amount
        )

        tax_amount = (
            taxable_amount * tax_rate / 100
        )


        # ==========================================
        # CALCULATE FINAL TOTAL
        # ==========================================

        total_amount = (
            taxable_amount + tax_amount
        )


        # ==========================================
        # BILL DATE
        # ==========================================

        bill_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


        # ==========================================
        # INSERT BILL
        # ==========================================

        cursor.execute("""
            INSERT INTO bills (
                patient_id,
                consultation_fee,
                room_charge,
                laboratory_charge,
                medicine_charge,
                subtotal,
                discount,
                discount_amount,
                tax_rate,
                tax_amount,
                total_amount,
                payment_status,
                bill_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            consultation_fee,
            room_charge,
            laboratory_charge,
            medicine_charge,
            subtotal,
            discount,
            discount_amount,
            tax_rate,
            tax_amount,
            total_amount,
            "Pending",
            bill_date
        ))


        bill_id = cursor.lastrowid

        connection.commit()


        # ==========================================
        # DISPLAY SUCCESS
        # ==========================================

        print("\nBill created successfully!")
        print(f"Bill ID: {bill_id}")
        print(f"Subtotal: ₹{subtotal:.2f}")
        print(f"Discount: ₹{discount_amount:.2f}")
        print(f"Tax: ₹{tax_amount:.2f}")
        print(f"Total Amount: ₹{total_amount:.2f}")
        print("Payment Status: Pending")


        return bill_id


    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return None


    finally:

        connection.close()


def view_bills():
    """Display all hospital bills."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                bills.bill_id,
                patients.first_name,
                patients.last_name,
                bills.consultation_fee,
                bills.room_charge,
                bills.laboratory_charge,
                bills.medicine_charge,
                bills.subtotal,
                bills.discount,
                bills.discount_amount,
                bills.tax_rate,
                bills.tax_amount,
                bills.total_amount,
                bills.payment_status,
                bills.bill_date

            FROM bills

            JOIN patients
                ON bills.patient_id =
                   patients.patient_id

            ORDER BY bills.bill_id
        """)

        bills = cursor.fetchall()


        if not bills:
            print("\nNo bills found.")
            return


        print("\n========== HOSPITAL BILLS ==========")


        for bill in bills:

            print("\n--------------------------------")
            print(f"Bill ID: {bill[0]}")
            print(f"Patient: {bill[1]} {bill[2]}")

            print(
                f"Consultation Fee: "
                f"₹{bill[3]:.2f}"
            )

            print(
                f"Room Charge: "
                f"₹{bill[4]:.2f}"
            )

            print(
                f"Laboratory Charge: "
                f"₹{bill[5]:.2f}"
            )

            print(
                f"Medicine Charge: "
                f"₹{bill[6]:.2f}"
            )

            print(
                f"Subtotal: "
                f"₹{bill[7]:.2f}"
            )

            print(
                f"Discount ({bill[8]}%): "
                f"₹{bill[9]:.2f}"
            )

            print(
                f"Tax ({bill[10]}%): "
                f"₹{bill[11]:.2f}"
            )

            print(
                f"Total Amount: "
                f"₹{bill[12]:.2f}"
            )

            print(
                f"Payment Status: "
                f"{bill[13]}"
            )

            print(
                f"Bill Date: "
                f"{bill[14]}"
            )


    except sqlite3.Error as error:

        print("\nDatabase error:", error)


    finally:

        connection.close()


def update_payment_status(
    bill_id,
    payment_status
):
    """Update the payment status of a bill."""

    valid_statuses = [
        "Pending",
        "Paid",
        "Partially Paid",
        "Cancelled"
    ]

    if payment_status not in valid_statuses:

        print("\nInvalid payment status!")

        print(
            "Use one of:",
            ", ".join(valid_statuses)
        )

        return False


    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT bill_id
            FROM bills
            WHERE bill_id = ?
        """, (bill_id,))

        bill = cursor.fetchone()


        if not bill:

            print("\nBill not found.")

            return False


        cursor.execute("""
            UPDATE bills
            SET payment_status = ?
            WHERE bill_id = ?
        """, (
            payment_status,
            bill_id
        ))


        connection.commit()


        print(
            "\nPayment status updated successfully!"
        )

        print(f"Bill ID: {bill_id}")
        print(
            f"Payment Status: {payment_status}"
        )


        return True


    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

        return False


    finally:

        connection.close()


def view_patient_bills(patient_id):
    """Display all bills for one patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

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


        cursor.execute("""
            SELECT
                bill_id,
                total_amount,
                payment_status,
                bill_date
            FROM bills
            WHERE patient_id = ?
            ORDER BY bill_date DESC
        """, (patient_id,))

        bills = cursor.fetchall()


        print(
            "\n========== PATIENT BILL HISTORY =========="
        )

        print(
            f"Patient: {patient[0]} {patient[1]}"
        )


        if not bills:

            print("\nNo bills found for this patient.")

            return


        for bill in bills:

            print("\n--------------------------------")

            print(f"Bill ID: {bill[0]}")

            print(
                f"Total Amount: "
                f"₹{bill[1]:.2f}"
            )

            print(
                f"Payment Status: {bill[2]}"
            )

            print(
                f"Bill Date: {bill[3]}"
            )


    except sqlite3.Error as error:

        print("\nDatabase error:", error)


    finally:

        connection.close()