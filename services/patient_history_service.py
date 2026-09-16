import sqlite3

from database import get_connection


def view_patient_transaction_history(patient_id):
    """
    Display complete transaction history
    of a patient.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==========================================
        # PATIENT INFORMATION
        # ==========================================

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

            print("\nPatient not found.")

            return


        # ==========================================
        # PATIENT HEADER
        # ==========================================

        print("\n")
        print("=" * 60)
        print("          COMPLETE PATIENT HISTORY")
        print("=" * 60)

        print(f"Patient ID: {patient[0]}")
        print(f"Name: {patient[1]} {patient[2]}")
        print(f"Gender: {patient[3]}")
        print(f"Date of Birth: {patient[4]}")
        print(f"Phone: {patient[5]}")
        print(f"Email: {patient[6]}")
        print(f"Blood Group: {patient[7]}")
        print(f"Registration Date: {patient[8]}")


        # ==========================================
        # APPOINTMENTS
        # ==========================================

        print("\n")
        print("=" * 60)
        print("APPOINTMENT HISTORY")
        print("=" * 60)

        cursor.execute("""
            SELECT
                appointments.appointment_id,
                doctors.first_name,
                doctors.last_name,
                appointments.appointment_date,
                appointments.appointment_time,
                appointments.reason,
                appointments.status
            FROM appointments

            JOIN doctors
                ON appointments.doctor_id =
                   doctors.doctor_id

            WHERE appointments.patient_id = ?

            ORDER BY appointments.appointment_date DESC
        """, (patient_id,))

        appointments = cursor.fetchall()

        if not appointments:

            print("No appointments found.")

        else:

            for appointment in appointments:

                print("\n------------------------------")

                print(
                    f"Appointment ID: "
                    f"{appointment[0]}"
                )

                print(
                    f"Doctor: Dr. "
                    f"{appointment[1]} "
                    f"{appointment[2]}"
                )

                print(
                    f"Date: {appointment[3]}"
                )

                print(
                    f"Time: {appointment[4]}"
                )

                print(
                    f"Reason: {appointment[5]}"
                )

                print(
                    f"Status: {appointment[6]}"
                )


        # ==========================================
        # MEDICAL HISTORY
        # ==========================================

        print("\n")
        print("=" * 60)
        print("MEDICAL HISTORY")
        print("=" * 60)

        cursor.execute("""
            SELECT
                medical_history.history_id,
                doctors.first_name,
                doctors.last_name,
                medical_history.record_date,
                medical_history.diagnosis,
                medical_history.treatment,
                medical_history.allergies,
                medical_history.notes

            FROM medical_history

            LEFT JOIN doctors
                ON medical_history.doctor_id =
                   doctors.doctor_id

            WHERE medical_history.patient_id = ?

            ORDER BY medical_history.record_date DESC
        """, (patient_id,))

        history = cursor.fetchall()

        if not history:

            print("No medical history found.")

        else:

            for record in history:

                print("\n------------------------------")

                print(
                    f"History ID: {record[0]}"
                )

                if record[1]:

                    print(
                        f"Doctor: Dr. "
                        f"{record[1]} {record[2]}"
                    )

                print(
                    f"Date: {record[3]}"
                )

                print(
                    f"Diagnosis: {record[4]}"
                )

                print(
                    f"Treatment: {record[5]}"
                )

                print(
                    f"Allergies: {record[6]}"
                )

                print(
                    f"Notes: {record[7]}"
                )


        # ==========================================
        # LABORATORY TEST HISTORY
        # ==========================================

        print("\n")
        print("=" * 60)
        print("LABORATORY TEST HISTORY")
        print("=" * 60)

        cursor.execute("""
            SELECT
                laboratory_tests.test_id,
                laboratory_tests.test_name,
                laboratory_tests.test_date,
                laboratory_tests.result,
                laboratory_tests.status,
                laboratory_tests.notes

            FROM laboratory_tests

            WHERE laboratory_tests.patient_id = ?

            ORDER BY laboratory_tests.test_date DESC
        """, (patient_id,))

        tests = cursor.fetchall()

        if not tests:

            print("No laboratory tests found.")

        else:

            for test in tests:

                print("\n------------------------------")

                print(
                    f"Test ID: {test[0]}"
                )

                print(
                    f"Test Name: {test[1]}"
                )

                print(
                    f"Date: {test[2]}"
                )

                print(
                    f"Result: {test[3]}"
                )

                print(
                    f"Status: {test[4]}"
                )

                print(
                    f"Notes: {test[5]}"
                )


        # ==========================================
        # ADMISSION HISTORY
        # ==========================================

        print("\n")
        print("=" * 60)
        print("ADMISSION / DISCHARGE HISTORY")
        print("=" * 60)

        cursor.execute("""
            SELECT
                admissions.admission_id,
                rooms.room_number,
                rooms.room_type,
                doctors.first_name,
                doctors.last_name,
                admissions.admission_date,
                admissions.discharge_date,
                admissions.diagnosis,
                admissions.status

            FROM admissions

            JOIN rooms
                ON admissions.room_id =
                   rooms.room_id

            LEFT JOIN doctors
                ON admissions.doctor_id =
                   doctors.doctor_id

            WHERE admissions.patient_id = ?

            ORDER BY admissions.admission_date DESC
        """, (patient_id,))

        admissions = cursor.fetchall()

        if not admissions:

            print("No admission records found.")

        else:

            for admission in admissions:

                print("\n------------------------------")

                print(
                    f"Admission ID: "
                    f"{admission[0]}"
                )

                print(
                    f"Room: {admission[1]}"
                )

                print(
                    f"Room Type: {admission[2]}"
                )

                if admission[3]:

                    print(
                        f"Doctor: Dr. "
                        f"{admission[3]} "
                        f"{admission[4]}"
                    )

                print(
                    f"Admission Date: "
                    f"{admission[5]}"
                )

                print(
                    f"Discharge Date: "
                    f"{admission[6]}"
                )

                print(
                    f"Diagnosis: "
                    f"{admission[7]}"
                )

                print(
                    f"Status: "
                    f"{admission[8]}"
                )


        # ==========================================
        # BILL HISTORY
        # ==========================================

        print("\n")
        print("=" * 60)
        print("BILLING HISTORY")
        print("=" * 60)

        cursor.execute("""
            SELECT
                bill_id,
                consultation_fee,
                room_charge,
                laboratory_charge,
                medicine_charge,
                discount_amount,
                tax_amount,
                total_amount,
                payment_status,
                bill_date

            FROM bills

            WHERE patient_id = ?

            ORDER BY bill_date DESC
        """, (patient_id,))

        bills = cursor.fetchall()

        if not bills:

            print("No billing records found.")

        else:

            for bill in bills:

                print("\n------------------------------")

                print(
                    f"Bill ID: {bill[0]}"
                )

                print(
                    f"Consultation: "
                    f"₹{bill[1]:.2f}"
                )

                print(
                    f"Room: "
                    f"₹{bill[2]:.2f}"
                )

                print(
                    f"Laboratory: "
                    f"₹{bill[3]:.2f}"
                )

                print(
                    f"Medicines: "
                    f"₹{bill[4]:.2f}"
                )

                print(
                    f"Discount: "
                    f"₹{bill[5]:.2f}"
                )

                print(
                    f"Tax: "
                    f"₹{bill[6]:.2f}"
                )

                print(
                    f"Total: "
                    f"₹{bill[7]:.2f}"
                )

                print(
                    f"Payment Status: "
                    f"{bill[8]}"
                )

                print(
                    f"Bill Date: "
                    f"{bill[9]}"
                )


        print("\n")
        print("=" * 60)
        print("       END OF PATIENT HISTORY")
        print("=" * 60)


    except sqlite3.Error as error:

        print("\nDatabase error:", error)


    finally:

        connection.close()