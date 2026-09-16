import sqlite3
from datetime import datetime, timedelta

from database import get_connection


# ============================================================
# ADD MEDICINE
# ============================================================

def add_medicine(
    name,
    manufacturer,
    price,
    stock_quantity,
    expiry_date,
    reorder_level=10
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Validate price
        if price < 0:
            print("\nPrice cannot be negative.")
            return False

        # Validate stock
        if stock_quantity < 0:
            print("\nStock quantity cannot be negative.")
            return False

        # Validate reorder level
        if reorder_level < 0:
            print("\nReorder level cannot be negative.")
            return False

        # Validate expiry date
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            print("\nInvalid expiry date.")
            print("Please use YYYY-MM-DD format.")
            return False

        cursor.execute("""
            INSERT INTO medicines (
                name,
                manufacturer,
                price,
                stock_quantity,
                expiry_date,
                reorder_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            manufacturer,
            price,
            stock_quantity,
            expiry_date,
            reorder_level
        ))

        connection.commit()

        print("\nMedicine added successfully!")
        print(f"Medicine ID: {cursor.lastrowid}")

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# VIEW ALL MEDICINES
# ============================================================

def view_medicines():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                medicine_id,
                name,
                manufacturer,
                price,
                stock_quantity,
                expiry_date,
                reorder_level
            FROM medicines
            ORDER BY medicine_id
        """)

        medicines = cursor.fetchall()

        if not medicines:
            print("\nNo medicines found.")
            return

        print("\n========== MEDICINE LIST ==========")

        for medicine in medicines:
            print("----------------------------------------")
            print(f"Medicine ID: {medicine[0]}")
            print(f"Name: {medicine[1]}")
            print(f"Manufacturer: {medicine[2]}")
            print(f"Price: ₹{medicine[3]}")
            print(f"Stock Quantity: {medicine[4]}")
            print(f"Expiry Date: {medicine[5]}")
            print(f"Reorder Level: {medicine[6]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# UPDATE MEDICINE STOCK
# ============================================================

def update_medicine_stock(medicine_id, quantity_change):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                name,
                stock_quantity
            FROM medicines
            WHERE medicine_id = ?
        """, (medicine_id,))

        medicine = cursor.fetchone()

        if not medicine:
            print("\nMedicine not found.")
            return False

        medicine_name = medicine[0]
        current_stock = medicine[1]

        new_stock = current_stock + quantity_change

        if new_stock < 0:
            print("\nStock update failed!")
            print("Insufficient medicine stock.")
            print(f"Current stock: {current_stock}")
            return False

        cursor.execute("""
            UPDATE medicines
            SET stock_quantity = ?
            WHERE medicine_id = ?
        """, (
            new_stock,
            medicine_id
        ))

        connection.commit()

        print("\nMedicine stock updated successfully!")
        print(f"Medicine: {medicine_name}")
        print(f"Old Stock: {current_stock}")
        print(f"New Stock: {new_stock}")

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# LOW STOCK MEDICINES
# ============================================================

def check_low_stock():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                medicine_id,
                name,
                stock_quantity,
                reorder_level
            FROM medicines
            WHERE stock_quantity <= reorder_level
            ORDER BY stock_quantity ASC
        """)

        medicines = cursor.fetchall()

        if not medicines:
            print("\nNo low-stock medicines found.")
            return

        print("\n========== LOW STOCK ALERT ==========")

        for medicine in medicines:
            print("----------------------------------------")
            print(f"Medicine ID: {medicine[0]}")
            print(f"Name: {medicine[1]}")
            print(f"Current Stock: {medicine[2]}")
            print(f"Reorder Level: {medicine[3]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# NEAR EXPIRY MEDICINES
# ============================================================

def check_near_expiry(days=30):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        today = datetime.now().date()
        future_date = today + timedelta(days=days)

        cursor.execute("""
            SELECT
                medicine_id,
                name,
                expiry_date,
                stock_quantity
            FROM medicines
            ORDER BY expiry_date
        """)

        medicines = cursor.fetchall()

        near_expiry_medicines = []

        for medicine in medicines:

            expiry_date_string = medicine[2]

            if not expiry_date_string:
                print(
                    f"\nWarning: Medicine ID {medicine[0]} "
                    "has no expiry date."
                )
                continue

            try:
                expiry_date = datetime.strptime(
                    str(expiry_date_string),
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                print(
                    f"\nWarning: Medicine ID {medicine[0]} "
                    f"has invalid expiry date: "
                    f"{medicine[2]}"
                )
                continue

            if today <= expiry_date <= future_date:
                near_expiry_medicines.append(medicine)

        if not near_expiry_medicines:
            print(
                f"\nNo medicines expiring within "
                f"{days} days."
            )
            return

        print(
            f"\n========== MEDICINES EXPIRING "
            f"WITHIN {days} DAYS =========="
        )

        for medicine in near_expiry_medicines:
            print("----------------------------------------")
            print(f"Medicine ID: {medicine[0]}")
            print(f"Name: {medicine[1]}")
            print(f"Expiry Date: {medicine[2]}")
            print(f"Stock Quantity: {medicine[3]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# EXPIRED MEDICINES
# ============================================================

def check_expired_medicines():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        today = datetime.now().date()

        cursor.execute("""
            SELECT
                medicine_id,
                name,
                expiry_date,
                stock_quantity
            FROM medicines
            ORDER BY expiry_date
        """)

        medicines = cursor.fetchall()

        expired_medicines = []

        for medicine in medicines:

            expiry_date_string = medicine[2]

            if not expiry_date_string:
                continue

            try:
                expiry_date = datetime.strptime(
                    str(expiry_date_string),
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                print(
                    f"\nWarning: Medicine ID {medicine[0]} "
                    f"has invalid expiry date: "
                    f"{medicine[2]}"
                )
                continue

            if expiry_date < today:
                expired_medicines.append(medicine)

        if not expired_medicines:
            print("\nNo expired medicines found.")
            return

        print("\n========== EXPIRED MEDICINES ==========")

        for medicine in expired_medicines:
            print("----------------------------------------")
            print(f"Medicine ID: {medicine[0]}")
            print(f"Name: {medicine[1]}")
            print(f"Expiry Date: {medicine[2]}")
            print(f"Stock Quantity: {medicine[3]}")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

