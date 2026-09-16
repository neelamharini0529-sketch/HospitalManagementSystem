import sqlite3
from datetime import datetime

from database import get_connection


# ============================================================
# ADD ROOM
# ============================================================

def add_room(room_number, room_type, daily_charge):
    """Add a new hospital room."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        room_number = room_number.strip()
        room_type = room_type.strip()

        if not room_number:
            print("\nRoom number cannot be empty.")
            return False

        if not room_type:
            print("\nRoom type cannot be empty.")
            return False

        if daily_charge < 0:
            print("\nDaily charge cannot be negative.")
            return False

        cursor.execute("""
            SELECT room_id
            FROM rooms
            WHERE room_number = ?
        """, (room_number,))

        existing_room = cursor.fetchone()

        if existing_room:
            print("\nRoom already exists.")
            return False

        cursor.execute("""
            INSERT INTO rooms (
                room_number,
                room_type,
                daily_charge,
                status
            )
            VALUES (?, ?, ?, ?)
        """, (
            room_number,
            room_type,
            daily_charge,
            "Available"
        ))

        connection.commit()

        print("\nRoom added successfully!")
        print(f"Room Number : {room_number}")
        print(f"Room Type   : {room_type}")
        print(f"Daily Charge: ₹{daily_charge:.2f}")
        print("Status      : Available")

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# VIEW ALL ROOMS
# ============================================================

def view_rooms():
    """Display all hospital rooms."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                room_id,
                room_number,
                room_type,
                daily_charge,
                status
            FROM rooms
            ORDER BY room_id
        """)

        rooms = cursor.fetchall()

        if not rooms:
            print("\nNo rooms found.")
            return

        print("\n")
        print("=" * 75)
        print("                         ALL ROOMS")
        print("=" * 75)

        print(
            f"{'ID':<5}"
            f"{'Room No.':<12}"
            f"{'Type':<18}"
            f"{'Daily Charge':<18}"
            f"{'Status':<15}"
        )

        print("-" * 75)

        for room in rooms:
            print(
                f"{room[0]:<5}"
                f"{room[1]:<12}"
                f"{room[2]:<18}"
                f"₹{room[3]:<17.2f}"
                f"{room[4]:<15}"
            )

        print("=" * 75)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# VIEW AVAILABLE ROOMS
# ============================================================

def view_available_rooms():
    """Display only available rooms."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                room_id,
                room_number,
                room_type,
                daily_charge
            FROM rooms
            WHERE status = 'Available'
            ORDER BY room_id
        """)

        rooms = cursor.fetchall()

        if not rooms:
            print("\nNo available rooms found.")
            return

        print("\n")
        print("=" * 70)
        print("                     AVAILABLE ROOMS")
        print("=" * 70)

        print(
            f"{'ID':<5}"
            f"{'Room No.':<12}"
            f"{'Type':<20}"
            f"{'Daily Charge':<15}"
        )

        print("-" * 70)

        for room in rooms:
            print(
                f"{room[0]:<5}"
                f"{room[1]:<12}"
                f"{room[2]:<20}"
                f"₹{room[3]:<14.2f}"
            )

        print("=" * 70)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# MANUAL PATIENT ADMISSION
# ============================================================

def admit_patient(
    patient_id,
    room_id,
    doctor_id=None,
    diagnosis=None
):
    """Admit a patient into a specific room."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Check patient
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nAdmission failed!")
            print("Patient does not exist.")
            return False

        # ----------------------------------------------------
        # Check whether patient is already admitted
        # ----------------------------------------------------

        cursor.execute("""
            SELECT admission_id
            FROM admissions
            WHERE patient_id = ?
              AND status = 'Admitted'
        """, (patient_id,))

        existing_admission = cursor.fetchone()

        if existing_admission:
            print("\nAdmission failed!")
            print("Patient is already admitted.")
            print(f"Admission ID: {existing_admission[0]}")
            return False

        # ----------------------------------------------------
        # Check room
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                room_id,
                room_number,
                room_type,
                daily_charge,
                status
            FROM rooms
            WHERE room_id = ?
        """, (room_id,))

        room = cursor.fetchone()

        if not room:
            print("\nAdmission failed!")
            print("Room does not exist.")
            return False

        if room[4] != "Available":
            print("\nAdmission failed!")
            print("Selected room is not available.")
            print(f"Room Status: {room[4]}")
            return False

        # ----------------------------------------------------
        # Check doctor if provided
        # ----------------------------------------------------

        doctor = None

        if doctor_id is not None:

            cursor.execute("""
                SELECT
                    doctor_id,
                    first_name,
                    last_name
                FROM doctors
                WHERE doctor_id = ?
            """, (doctor_id,))

            doctor = cursor.fetchone()

            if not doctor:
                print("\nAdmission failed!")
                print("Doctor does not exist.")
                return False

        # ----------------------------------------------------
        # Admission date
        # ----------------------------------------------------

        admission_date = datetime.now().strftime("%Y-%m-%d")

        # ----------------------------------------------------
        # Create admission
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Mark room as occupied
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE rooms
            SET status = 'Occupied'
            WHERE room_id = ?
        """, (room_id,))

        connection.commit()

        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print("\n")
        print("=" * 60)
        print("              PATIENT ADMITTED SUCCESSFULLY")
        print("=" * 60)

        print(f"Admission ID : {admission_id}")
        print(f"Patient      : {patient[1]} {patient[2]}")
        print(f"Room Number  : {room[1]}")
        print(f"Room Type    : {room[2]}")
        print(f"Daily Charge : ₹{room[3]:.2f}")
        print(f"Admission Date: {admission_date}")

        if doctor:
            print(f"Doctor       : Dr. {doctor[1]} {doctor[2]}")

        print(f"Diagnosis    : {diagnosis}")
        print("Status       : Admitted")

        print("=" * 60)

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# AUTOMATIC ROOM ALLOCATION
# ============================================================

def auto_allocate_room(
    patient_id,
    doctor_id=None,
    diagnosis=None,
    room_type=None
):
    """
    Automatically find an available room
    and admit the patient.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Check patient
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nAutomatic admission failed!")
            print("Patient does not exist.")
            return False

        # ----------------------------------------------------
        # Check existing admission
        # ----------------------------------------------------

        cursor.execute("""
            SELECT admission_id
            FROM admissions
            WHERE patient_id = ?
              AND status = 'Admitted'
        """, (patient_id,))

        existing_admission = cursor.fetchone()

        if existing_admission:
            print("\nAutomatic admission failed!")
            print("Patient is already admitted.")
            print(f"Admission ID: {existing_admission[0]}")
            return False

        # ----------------------------------------------------
        # Check doctor if provided
        # ----------------------------------------------------

        doctor = None

        if doctor_id is not None:

            cursor.execute("""
                SELECT
                    doctor_id,
                    first_name,
                    last_name
                FROM doctors
                WHERE doctor_id = ?
            """, (doctor_id,))

            doctor = cursor.fetchone()

            if not doctor:
                print("\nAutomatic admission failed!")
                print("Doctor does not exist.")
                return False

        # ----------------------------------------------------
        # Find available room
        # ----------------------------------------------------

        if room_type:

            cursor.execute("""
                SELECT
                    room_id,
                    room_number,
                    room_type,
                    daily_charge
                FROM rooms
                WHERE status = 'Available'
                  AND room_type = ?
                ORDER BY room_id
                LIMIT 1
            """, (room_type,))

        else:

            cursor.execute("""
                SELECT
                    room_id,
                    room_number,
                    room_type,
                    daily_charge
                FROM rooms
                WHERE status = 'Available'
                ORDER BY room_id
                LIMIT 1
            """)

        room = cursor.fetchone()

        if not room:

            print("\nAutomatic admission failed!")

            if room_type:
                print(f"No available {room_type} room found.")
            else:
                print("No available rooms found.")

            return False

        # ----------------------------------------------------
        # Create admission
        # ----------------------------------------------------

        admission_date = datetime.now().strftime("%Y-%m-%d")

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
            room[0],
            doctor_id,
            admission_date,
            diagnosis,
            "Admitted"
        ))

        admission_id = cursor.lastrowid

        # ----------------------------------------------------
        # Occupy room
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE rooms
            SET status = 'Occupied'
            WHERE room_id = ?
        """, (room[0],))

        connection.commit()

        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print("\n")
        print("=" * 65)
        print("        AUTOMATIC ROOM ALLOCATION SUCCESSFUL")
        print("=" * 65)

        print(f"Admission ID : {admission_id}")
        print(f"Patient      : {patient[1]} {patient[2]}")
        print(f"Room ID      : {room[0]}")
        print(f"Room Number  : {room[1]}")
        print(f"Room Type    : {room[2]}")
        print(f"Daily Charge : ₹{room[3]:.2f}")
        print(f"Admission Date: {admission_date}")

        if doctor:
            print(f"Doctor       : Dr. {doctor[1]} {doctor[2]}")

        print(f"Diagnosis    : {diagnosis}")
        print("Status       : Admitted")

        print("=" * 65)

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# VIEW CURRENT ADMISSIONS
# ============================================================

def view_current_admissions():
    """Display all currently admitted patients."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                a.admission_id,
                p.first_name || ' ' || p.last_name,
                r.room_number,
                r.room_type,
                d.first_name || ' ' || d.last_name,
                a.admission_date,
                a.diagnosis,
                a.status
            FROM admissions a

            JOIN patients p
                ON a.patient_id = p.patient_id

            JOIN rooms r
                ON a.room_id = r.room_id

            LEFT JOIN doctors d
                ON a.doctor_id = d.doctor_id

            WHERE a.status = 'Admitted'

            ORDER BY a.admission_id
        """)

        admissions = cursor.fetchall()

        if not admissions:
            print("\nNo current admissions found.")
            return

        print("\n")
        print("=" * 110)
        print("                         CURRENT ADMISSIONS")
        print("=" * 110)

        print(
            f"{'ID':<5}"
            f"{'Patient':<22}"
            f"{'Room':<10}"
            f"{'Type':<15}"
            f"{'Doctor':<22}"
            f"{'Date':<12}"
            f"{'Status':<12}"
        )

        print("-" * 110)

        for admission in admissions:

            doctor_name = (
                admission[4]
                if admission[4]
                else "Not Assigned"
            )

            print(
                f"{admission[0]:<5}"
                f"{admission[1]:<22}"
                f"{admission[2]:<10}"
                f"{admission[3]:<15}"
                f"{doctor_name:<22}"
                f"{admission[5]:<12}"
                f"{admission[7]:<12}"
            )

            print(f"Diagnosis: {admission[6]}")

        print("=" * 110)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# DISCHARGE PATIENT
# ============================================================

def discharge_patient(admission_id):
    """Discharge a patient and make the room available."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                a.admission_id,
                a.patient_id,
                a.room_id,
                a.admission_date,
                a.status,
                p.first_name,
                p.last_name,
                r.room_number
            FROM admissions a

            JOIN patients p
                ON a.patient_id = p.patient_id

            JOIN rooms r
                ON a.room_id = r.room_id

            WHERE a.admission_id = ?
        """, (admission_id,))

        admission = cursor.fetchone()

        if not admission:
            print("\nDischarge failed!")
            print("Admission does not exist.")
            return False

        if admission[4] != "Admitted":
            print("\nPatient is not currently admitted.")
            print(f"Current status: {admission[4]}")
            return False

        discharge_date = datetime.now().strftime("%Y-%m-%d")

        # ----------------------------------------------------
        # Update admission
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE admissions
            SET
                discharge_date = ?,
                status = 'Discharged'
            WHERE admission_id = ?
        """, (
            discharge_date,
            admission_id
        ))

        # ----------------------------------------------------
        # Make room available
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE rooms
            SET status = 'Available'
            WHERE room_id = ?
        """, (admission[2],))

        connection.commit()

        print("\n")
        print("=" * 60)
        print("             PATIENT DISCHARGED SUCCESSFULLY")
        print("=" * 60)

        print(f"Admission ID : {admission_id}")
        print(f"Patient      : {admission[5]} {admission[6]}")
        print(f"Room Number  : {admission[7]}")
        print(f"Admission Date: {admission[3]}")
        print(f"Discharge Date: {discharge_date}")
        print("Status       : Discharged")

        print("=" * 60)

        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("\nDatabase error:", error)
        return False

    finally:
        connection.close()


# ============================================================
# VIEW PATIENT ADMISSION HISTORY
# ============================================================

def view_patient_admissions(patient_id):
    """Display complete admission history of a patient."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Check patient
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nPatient does not exist.")
            return

        # ----------------------------------------------------
        # Get admission history
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                a.admission_id,
                r.room_number,
                r.room_type,
                d.first_name || ' ' || d.last_name,
                a.admission_date,
                a.discharge_date,
                a.diagnosis,
                a.status
            FROM admissions a

            JOIN rooms r
                ON a.room_id = r.room_id

            LEFT JOIN doctors d
                ON a.doctor_id = d.doctor_id

            WHERE a.patient_id = ?

            ORDER BY a.admission_id
        """, (patient_id,))

        admissions = cursor.fetchall()

        if not admissions:
            print("\nNo admission history found.")
            return

        print("\n")
        print("=" * 90)
        print(
            f"       ADMISSION HISTORY - "
            f"{patient[1]} {patient[2]}"
        )
        print("=" * 90)

        for admission in admissions:

            doctor_name = (
                admission[3]
                if admission[3]
                else "Not Assigned"
            )

            discharge_date = (
                admission[5]
                if admission[5]
                else "Not Discharged"
            )

            print(f"\nAdmission ID  : {admission[0]}")
            print(f"Room Number   : {admission[1]}")
            print(f"Room Type     : {admission[2]}")
            print(f"Doctor        : {doctor_name}")
            print(f"Admission Date: {admission[4]}")
            print(f"Discharge Date: {discharge_date}")
            print(f"Diagnosis     : {admission[6]}")
            print(f"Status        : {admission[7]}")
            print("-" * 90)

        print("=" * 90)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()