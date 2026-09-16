import sqlite3
from database import get_connection


# ============================================================
# PATIENT REPORT
# ============================================================

def patient_report():
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

        print("\n")
        print("=" * 70)
        print("                    PATIENT REPORT")
        print("=" * 70)

        for patient in patients:

            print("\n--------------------------------------------")

            print(f"Patient ID       : {patient[0]}")
            print(f"Name             : {patient[1]} {patient[2]}")
            print(f"Gender           : {patient[3]}")
            print(f"Date of Birth    : {patient[4]}")
            print(f"Phone            : {patient[5]}")
            print(f"Email            : {patient[6]}")
            print(f"Blood Group      : {patient[7]}")
            print(f"Registration Date: {patient[8]}")

        print("\n" + "=" * 70)
        print(f"Total Patients: {len(patients)}")
        print("=" * 70)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# DOCTOR REPORT
# ============================================================

def doctor_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                d.doctor_id,
                d.first_name,
                d.last_name,
                d.gender,
                d.phone,
                d.email,
                d.specialization,
                dep.name,
                d.consultation_fee
            FROM doctors d
            LEFT JOIN departments dep
                ON d.department_id = dep.department_id
            ORDER BY d.doctor_id
        """)

        doctors = cursor.fetchall()

        if not doctors:
            print("\nNo doctors found.")
            return

        print("\n")
        print("=" * 70)
        print("                     DOCTOR REPORT")
        print("=" * 70)

        for doctor in doctors:

            print("\n--------------------------------------------")

            print(f"Doctor ID        : {doctor[0]}")
            print(f"Name             : {doctor[1]} {doctor[2]}")
            print(f"Gender           : {doctor[3]}")
            print(f"Phone            : {doctor[4]}")
            print(f"Email            : {doctor[5]}")
            print(f"Specialization   : {doctor[6]}")
            print(f"Department       : {doctor[7]}")
            print(f"Consultation Fee : ₹{doctor[8]:.2f}")

        print("\n" + "=" * 70)
        print(f"Total Doctors: {len(doctors)}")
        print("=" * 70)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# APPOINTMENT REPORT
# ============================================================

def appointment_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                a.appointment_id,
                p.first_name || ' ' || p.last_name,
                d.first_name || ' ' || d.last_name,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date, a.appointment_time
        """)

        appointments = cursor.fetchall()

        if not appointments:
            print("\nNo appointments found.")
            return

        print("\n")
        print("=" * 75)
        print("                       APPOINTMENT REPORT")
        print("=" * 75)

        for appointment in appointments:

            print("\n--------------------------------------------")

            print(f"Appointment ID : {appointment[0]}")
            print(f"Patient        : {appointment[1]}")
            print(f"Doctor         : {appointment[2]}")
            print(f"Date           : {appointment[3]}")
            print(f"Time           : {appointment[4]}")
            print(f"Reason         : {appointment[5]}")
            print(f"Status         : {appointment[6]}")

        print("\n" + "=" * 75)
        print(f"Total Appointments: {len(appointments)}")
        print("=" * 75)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# ADMISSION REPORT
# ============================================================

def admission_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                a.admission_id,
                p.first_name || ' ' || p.last_name,
                r.room_number,
                d.first_name || ' ' || d.last_name,
                a.admission_date,
                a.discharge_date,
                a.diagnosis,
                a.status
            FROM admissions a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN rooms r
                ON a.room_id = r.room_id
            LEFT JOIN doctors d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.admission_date DESC
        """)

        admissions = cursor.fetchall()

        if not admissions:
            print("\nNo admission records found.")
            return

        print("\n")
        print("=" * 75)
        print("                       ADMISSION REPORT")
        print("=" * 75)

        for admission in admissions:

            print("\n--------------------------------------------")

            print(f"Admission ID   : {admission[0]}")
            print(f"Patient        : {admission[1]}")
            print(f"Room Number    : {admission[2]}")
            print(f"Doctor         : {admission[3]}")
            print(f"Admission Date : {admission[4]}")
            print(f"Discharge Date : {admission[5]}")
            print(f"Diagnosis      : {admission[6]}")
            print(f"Status         : {admission[7]}")

        print("\n" + "=" * 75)
        print(f"Total Admissions: {len(admissions)}")
        print("=" * 75)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# PHARMACY STOCK REPORT
# ============================================================

def pharmacy_stock_report():
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
            ORDER BY name
        """)

        medicines = cursor.fetchall()

        if not medicines:
            print("\nNo medicines found.")
            return

        print("\n")
        print("=" * 80)
        print("                    PHARMACY STOCK REPORT")
        print("=" * 80)

        for medicine in medicines:

            print("\n--------------------------------------------")

            print(f"Medicine ID    : {medicine[0]}")
            print(f"Name           : {medicine[1]}")
            print(f"Manufacturer   : {medicine[2]}")
            print(f"Price          : ₹{medicine[3]:.2f}")
            print(f"Current Stock  : {medicine[4]}")
            print(f"Expiry Date    : {medicine[5]}")
            print(f"Reorder Level  : {medicine[6]}")

            if medicine[4] <= medicine[6]:
                print("Stock Status   : LOW STOCK")
            else:
                print("Stock Status   : Sufficient")

        print("\n" + "=" * 80)
        print(f"Total Medicines: {len(medicines)}")
        print("=" * 80)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# EXPIRED MEDICINE REPORT
# ============================================================

def expired_medicine_report():
    from datetime import datetime

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                medicine_id,
                name,
                manufacturer,
                stock_quantity,
                expiry_date
            FROM medicines
            ORDER BY expiry_date
        """)

        medicines = cursor.fetchall()

        expired_medicines = []

        for medicine in medicines:

            try:
                expiry_date = datetime.strptime(
                    str(medicine[4]),
                    "%Y-%m-%d"
                ).date()

                today = datetime.now().date()

                if expiry_date < today:
                    expired_medicines.append(medicine)

            except ValueError:
                print(
                    f"\nWarning: Invalid expiry date for "
                    f"Medicine ID {medicine[0]}: {medicine[4]}"
                )

        if not expired_medicines:
            print("\nNo expired medicines found.")
            return

        print("\n")
        print("=" * 80)
        print("                  EXPIRED MEDICINE REPORT")
        print("=" * 80)

        for medicine in expired_medicines:

            print("\n--------------------------------------------")

            print(f"Medicine ID   : {medicine[0]}")
            print(f"Name          : {medicine[1]}")
            print(f"Manufacturer  : {medicine[2]}")
            print(f"Current Stock : {medicine[3]}")
            print(f"Expiry Date   : {medicine[4]}")
            print("Status        : EXPIRED")

        print("\n" + "=" * 80)
        print(f"Total Expired Medicines: {len(expired_medicines)}")
        print("=" * 80)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# LABORATORY REPORT
# ============================================================

def laboratory_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                l.test_id,
                p.first_name || ' ' || p.last_name,
                d.first_name || ' ' || d.last_name,
                l.test_name,
                l.test_date,
                l.result,
                l.status,
                l.notes
            FROM laboratory_tests l
            JOIN patients p
                ON l.patient_id = p.patient_id
            LEFT JOIN doctors d
                ON l.doctor_id = d.doctor_id
            ORDER BY l.test_date DESC
        """)

        tests = cursor.fetchall()

        if not tests:
            print("\nNo laboratory tests found.")
            return

        print("\n")
        print("=" * 80)
        print("                     LABORATORY REPORT")
        print("=" * 80)

        for test in tests:

            print("\n--------------------------------------------")

            print(f"Test ID       : {test[0]}")
            print(f"Patient       : {test[1]}")
            print(f"Doctor        : {test[2]}")
            print(f"Test Name     : {test[3]}")
            print(f"Test Date     : {test[4]}")
            print(f"Result        : {test[5]}")
            print(f"Status        : {test[6]}")
            print(f"Notes         : {test[7]}")

        print("\n" + "=" * 80)
        print(f"Total Laboratory Tests: {len(tests)}")
        print("=" * 80)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# BILLING AND REVENUE REPORT
# ============================================================

def billing_revenue_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                bill_id,
                patient_id,
                consultation_fee,
                room_charge,
                laboratory_charge,
                medicine_charge,
                subtotal,
                discount_amount,
                tax_amount,
                total_amount,
                payment_status,
                bill_date
            FROM bills
            ORDER BY bill_date DESC
        """)

        bills = cursor.fetchall()

        if not bills:
            print("\nNo billing records found.")
            return

        print("\n")
        print("=" * 85)
        print("                    BILLING & REVENUE REPORT")
        print("=" * 85)

        total_revenue = 0
        paid_revenue = 0
        pending_amount = 0

        for bill in bills:

            print("\n--------------------------------------------")

            print(f"Bill ID             : {bill[0]}")
            print(f"Patient ID          : {bill[1]}")
            print(f"Consultation Fee    : ₹{bill[2]:.2f}")
            print(f"Room Charge         : ₹{bill[3]:.2f}")
            print(f"Laboratory Charge   : ₹{bill[4]:.2f}")
            print(f"Medicine Charge     : ₹{bill[5]:.2f}")
            print(f"Subtotal            : ₹{bill[6]:.2f}")
            print(f"Discount Amount     : ₹{bill[7]:.2f}")
            print(f"Tax Amount          : ₹{bill[8]:.2f}")
            print(f"Total Amount        : ₹{bill[9]:.2f}")
            print(f"Payment Status      : {bill[10]}")
            print(f"Bill Date           : {bill[11]}")

            total_revenue += bill[9]

            if bill[10] == "Paid":
                paid_revenue += bill[9]

            elif bill[10] == "Pending":
                pending_amount += bill[9]

        print("\n" + "=" * 85)
        print("                    REVENUE SUMMARY")
        print("=" * 85)

        print(f"Total Bills         : {len(bills)}")
        print(f"Total Bill Amount   : ₹{total_revenue:.2f}")
        print(f"Paid Revenue        : ₹{paid_revenue:.2f}")
        print(f"Pending Amount      : ₹{pending_amount:.2f}")

        print("=" * 85)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()

# ============================================================
# STAFF REPORT
# ============================================================

def staff_report():
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

        print("\n")
        print("=" * 80)
        print("                         STAFF REPORT")
        print("=" * 80)

        total_salary = 0

        for staff in staff_members:

            print("\n--------------------------------------------")

            print(f"Staff ID       : {staff[0]}")
            print(f"Name           : {staff[1]} {staff[2]}")
            print(f"Gender         : {staff[3]}")
            print(f"Phone          : {staff[4]}")
            print(f"Email          : {staff[5]}")
            print(f"Job Title      : {staff[6]}")
            print(f"Salary         : ₹{staff[7]:.2f}")

            total_salary += staff[7]

        print("\n" + "=" * 80)
        print(f"Total Staff Members : {len(staff_members)}")
        print(f"Total Salary        : ₹{total_salary:.2f}")
        print("=" * 80)

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


# ============================================================
# PATIENT TRANSACTION HISTORY
# ============================================================

def patient_transaction_history(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ====================================================
        # PATIENT INFORMATION
        # ====================================================

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
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        if not patient:
            print("\nPatient does not exist.")
            return

        print("\n")
        print("=" * 90)
        print("                    PATIENT TRANSACTION HISTORY")
        print("=" * 90)

        print("\nPATIENT INFORMATION")
        print("-" * 50)

        print(f"Patient ID       : {patient[0]}")
        print(f"Name             : {patient[1]} {patient[2]}")
        print(f"Gender           : {patient[3]}")
        print(f"Date of Birth    : {patient[4]}")
        print(f"Phone            : {patient[5]}")
        print(f"Email            : {patient[6]}")
        print(f"Blood Group      : {patient[7]}")
        print(f"Registration Date: {patient[8]}")

        # ====================================================
        # APPOINTMENTS
        # ====================================================

        print("\n")
        print("=" * 90)
        print("APPOINTMENT HISTORY")
        print("=" * 90)

        cursor.execute("""
            SELECT
                a.appointment_id,
                a.appointment_date,
                a.appointment_time,
                d.first_name,
                d.last_name,
                a.reason,
                a.status
            FROM appointments a
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date, a.appointment_time
        """, (patient_id,))

        appointments = cursor.fetchall()

        if appointments:

            for appointment in appointments:

                print("\n--------------------------------------------")

                print(f"Appointment ID : {appointment[0]}")
                print(f"Date           : {appointment[1]}")
                print(f"Time           : {appointment[2]}")
                print(f"Doctor         : Dr. {appointment[3]} {appointment[4]}")
                print(f"Reason         : {appointment[5]}")
                print(f"Status         : {appointment[6]}")

        else:
            print("\nNo appointment records found.")

        # ====================================================
        # MEDICAL HISTORY
        # ====================================================

        print("\n")
        print("=" * 90)
        print("MEDICAL HISTORY")
        print("=" * 90)

        cursor.execute("""
            SELECT
                mh.history_id,
                mh.record_date,
                d.first_name,
                d.last_name,
                mh.diagnosis,
                mh.treatment,
                mh.allergies,
                mh.notes
            FROM medical_history mh
            LEFT JOIN doctors d
                ON mh.doctor_id = d.doctor_id
            WHERE mh.patient_id = ?
            ORDER BY mh.record_date
        """, (patient_id,))

        history_records = cursor.fetchall()

        if history_records:

            for history in history_records:

                print("\n--------------------------------------------")

                print(f"History ID     : {history[0]}")
                print(f"Date           : {history[1]}")

                if history[2]:
                    print(f"Doctor         : Dr. {history[2]} {history[3]}")
                else:
                    print("Doctor         : Not specified")

                print(f"Diagnosis      : {history[4]}")
                print(f"Treatment      : {history[5]}")
                print(f"Allergies      : {history[6]}")
                print(f"Notes          : {history[7]}")

        else:
            print("\nNo medical history records found.")

        # ====================================================
        # LABORATORY HISTORY
        # ====================================================

        print("\n")
        print("=" * 90)
        print("LABORATORY TEST HISTORY")
        print("=" * 90)

        cursor.execute("""
            SELECT
                lt.test_id,
                lt.test_name,
                lt.test_date,
                d.first_name,
                d.last_name,
                lt.result,
                lt.status,
                lt.notes
            FROM laboratory_tests lt
            LEFT JOIN doctors d
                ON lt.doctor_id = d.doctor_id
            WHERE lt.patient_id = ?
            ORDER BY lt.test_date
        """, (patient_id,))

        laboratory_tests = cursor.fetchall()

        if laboratory_tests:

            for test in laboratory_tests:

                print("\n--------------------------------------------")

                print(f"Test ID        : {test[0]}")
                print(f"Test Name      : {test[1]}")
                print(f"Test Date      : {test[2]}")

                if test[3]:
                    print(f"Doctor         : Dr. {test[3]} {test[4]}")
                else:
                    print("Doctor         : Not specified")

                print(f"Result         : {test[5]}")
                print(f"Status         : {test[6]}")
                print(f"Notes          : {test[7]}")

        else:
            print("\nNo laboratory records found.")

        # ====================================================
        # ADMISSION HISTORY
        # ====================================================

        print("\n")
        print("=" * 90)
        print("ADMISSION / DISCHARGE HISTORY")
        print("=" * 90)

        cursor.execute("""
            SELECT
                a.admission_id,
                r.room_number,
                r.room_type,
                d.first_name,
                d.last_name,
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
            ORDER BY a.admission_date
        """, (patient_id,))

        admissions = cursor.fetchall()

        if admissions:

            for admission in admissions:

                print("\n--------------------------------------------")

                print(f"Admission ID   : {admission[0]}")
                print(f"Room Number    : {admission[1]}")
                print(f"Room Type      : {admission[2]}")

                if admission[3]:
                    print(f"Doctor         : Dr. {admission[3]} {admission[4]}")
                else:
                    print("Doctor         : Not specified")

                print(f"Admission Date : {admission[5]}")
                print(f"Discharge Date : {admission[6]}")
                print(f"Diagnosis      : {admission[7]}")
                print(f"Status         : {admission[8]}")

        else:
            print("\nNo admission records found.")

        # ====================================================
        # BILLING HISTORY
        # ====================================================

        print("\n")
        print("=" * 90)
        print("BILLING HISTORY")
        print("=" * 90)

        cursor.execute("""
            SELECT
                bill_id,
                consultation_fee,
                room_charge,
                laboratory_charge,
                medicine_charge,
                subtotal,
                discount_amount,
                tax_amount,
                total_amount,
                payment_status,
                bill_date
            FROM bills
            WHERE patient_id = ?
            ORDER BY bill_date
        """, (patient_id,))

        bills = cursor.fetchall()

        if bills:

            total_billed = 0
            total_paid = 0

            for bill in bills:

                print("\n--------------------------------------------")

                print(f"Bill ID            : {bill[0]}")
                print(f"Consultation Fee   : ₹{bill[1]:.2f}")
                print(f"Room Charge        : ₹{bill[2]:.2f}")
                print(f"Laboratory Charge  : ₹{bill[3]:.2f}")
                print(f"Medicine Charge    : ₹{bill[4]:.2f}")
                print(f"Subtotal           : ₹{bill[5]:.2f}")
                print(f"Discount Amount    : ₹{bill[6]:.2f}")
                print(f"Tax Amount         : ₹{bill[7]:.2f}")
                print(f"Total Amount       : ₹{bill[8]:.2f}")
                print(f"Payment Status     : {bill[9]}")
                print(f"Bill Date          : {bill[10]}")

                total_billed += bill[8]

                if bill[9] == "Paid":
                    total_paid += bill[8]

            print("\n--------------------------------------------")
            print(f"Total Billed       : ₹{total_billed:.2f}")
            print(f"Total Paid         : ₹{total_paid:.2f}")

        else:
            print("\nNo billing records found.")

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print("\n")
        print("=" * 90)
        print("PATIENT TRANSACTION SUMMARY")
        print("=" * 90)

        print(f"Appointments       : {len(appointments)}")
        print(f"Medical Records    : {len(history_records)}")
        print(f"Laboratory Tests   : {len(laboratory_tests)}")
        print(f"Admissions         : {len(admissions)}")
        print(f"Bills              : {len(bills)}")

        print("=" * 90)

    except sqlite3.Error as error:

        print("\nDatabase error:", error)

    finally:

        connection.close()


# ============================================================
# REPORT MENU
# ============================================================

def report_menu():

    while True:

        print("\n")
        print("=" * 60)
        print("                 REPORTS MENU")
        print("=" * 60)

        print("1. Patient Report")
        print("2. Doctor Report")
        print("3. Appointment Report")
        print("4. Admission Report")
        print("5. Pharmacy Stock Report")
        print("6. Expired Medicine Report")
        print("7. Laboratory Report")
        print("8. Billing Revenue Report")
        print("9. Staff Report")
        print("10. Patient Transaction History")
        print("11. Return to Main Menu")

        print("=" * 60)

        choice = input("Enter your choice: ").strip()

        # ----------------------------------------------------
        # PATIENT REPORT
        # ----------------------------------------------------

        if choice == "1":
            patient_report()

        # ----------------------------------------------------
        # DOCTOR REPORT
        # ----------------------------------------------------

        elif choice == "2":
            doctor_report()

        # ----------------------------------------------------
        # APPOINTMENT REPORT
        # ----------------------------------------------------

        elif choice == "3":
            appointment_report()

        # ----------------------------------------------------
        # ADMISSION REPORT
        # ----------------------------------------------------

        elif choice == "4":
            admission_report()

        # ----------------------------------------------------
        # PHARMACY STOCK REPORT
        # ----------------------------------------------------

        elif choice == "5":
            pharmacy_stock_report()

        # ----------------------------------------------------
        # EXPIRED MEDICINE REPORT
        # ----------------------------------------------------

        elif choice == "6":
            expired_medicine_report()

        # ----------------------------------------------------
        # LABORATORY REPORT
        # ----------------------------------------------------

        elif choice == "7":
            laboratory_report()

        # ----------------------------------------------------
        # BILLING REVENUE REPORT
        # ----------------------------------------------------

        elif choice == "8":
            billing_revenue_report()

        # ----------------------------------------------------
        # STAFF REPORT
        # ----------------------------------------------------

        elif choice == "9":
            staff_report()

        # ----------------------------------------------------
        # PATIENT TRANSACTION HISTORY
        # ----------------------------------------------------

        elif choice == "10":

            patient_id_input = input(
                "Enter patient ID: "
            ).strip()

            try:

                patient_id = int(patient_id_input)

                if patient_id <= 0:
                    print("\nPatient ID must be greater than 0.")
                    continue

                patient_transaction_history(patient_id)

            except ValueError:
                print("\nInvalid patient ID. Please enter a number.")

        # ----------------------------------------------------
        # RETURN TO MAIN MENU
        # ----------------------------------------------------

        elif choice == "11":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please select 1-11.")