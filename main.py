from database import create_tables

# ============================================================
# DASHBOARD
# ============================================================

from services.dashboard_service import show_dashboard


# ============================================================
# REPORTS
# ============================================================

from services.report_service import report_menu


# ============================================================
# PATIENT
# ============================================================

from services.patient_service import (
    register_patient,
    view_patients,
    search_patient,
    update_patient,
    delete_patient
)


# ============================================================
# DOCTOR
# ============================================================

from services.doctor_service import (
    add_doctor,
    view_doctors,
    search_doctor
)


# ============================================================
# APPOINTMENT
# ============================================================

from services.appointment_service import (
    schedule_appointment,
    view_appointments,
    update_appointment_status,
    cancel_appointment,
    view_patient_appointments
)


# ============================================================
# MEDICAL HISTORY
# ============================================================

from services.medical_history_service import (
    view_medical_history,
    view_patient_medical_history
)


# ============================================================
# LABORATORY
# ============================================================

from services.laboratory_service import (
    add_laboratory_test,
    view_laboratory_tests,
    update_test_result,
    view_patient_laboratory_history
)


# ============================================================
# BILLING
# ============================================================

from services.billing_service import (
    create_bill,
    view_bills,
    update_payment_status,
    view_patient_bills
)


# ============================================================
# PHARMACY
# ============================================================

from services.pharmacy_service import (
    add_medicine,
    view_medicines,
    update_medicine_stock,
    check_low_stock,
    check_near_expiry,
    check_expired_medicines
)


# ============================================================
# STAFF
# ============================================================

from services.staff_service import (
    add_staff,
    view_staff,
    search_staff_by_job,
    delete_staff
)


# ============================================================
# ROOM & ADMISSION
# ============================================================

from services.room_service import (
    add_room,
    view_rooms,
    view_available_rooms,
    admit_patient,
    auto_allocate_room,
    view_current_admissions,
    discharge_patient,
    view_patient_admissions
)


# ============================================================
# MEDICAL HISTORY MENU
# ============================================================

def medical_history_menu():

    while True:

        print("\n========== MEDICAL HISTORY MENU ==========")
        print("1. View all medical history")
        print("2. View patient medical history")
        print("3. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":

            view_medical_history()

        elif choice == "2":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                view_patient_medical_history(
                    patient_id
                )

            except ValueError:

                print("\nPlease enter a valid patient ID.")

        elif choice == "3":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# LABORATORY MENU
# ============================================================

def laboratory_menu():

    while True:

        print("\n========== LABORATORY MENU ==========")
        print("1. Add laboratory test")
        print("2. View all laboratory tests")
        print("3. Update test result")
        print("4. View patient laboratory history")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                test_name = input(
                    "Enter laboratory test name: "
                )

                test_date = input(
                    "Enter test date (YYYY-MM-DD): "
                )

                result = input(
                    "Enter test result: "
                )

                add_laboratory_test(
                    patient_id,
                    test_name,
                    test_date,
                    result
                )

            except ValueError:

                print("\nPlease enter valid values.")

        elif choice == "2":

            view_laboratory_tests()

        elif choice == "3":

            try:

                test_id = int(
                    input("Enter laboratory test ID: ")
                )

                result = input(
                    "Enter new test result: "
                )

                update_test_result(
                    test_id,
                    result
                )

            except ValueError:

                print("\nPlease enter a valid test ID.")

        elif choice == "4":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                view_patient_laboratory_history(
                    patient_id
                )

            except ValueError:

                print("\nPlease enter a valid patient ID.")

        elif choice == "5":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# APPOINTMENT MENU
# ============================================================

def appointment_menu():

    while True:

        print("\n========== APPOINTMENT MENU ==========")
        print("1. Schedule appointment")
        print("2. View all appointments")
        print("3. Update appointment status")
        print("4. Cancel appointment")
        print("5. View patient appointments")
        print("6. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                doctor_id = int(
                    input("Enter doctor ID: ")
                )

                appointment_date = input(
                    "Enter appointment date (YYYY-MM-DD): "
                )

                appointment_time = input(
                    "Enter appointment time (HH:MM): "
                )

                reason = input(
                    "Enter reason for appointment: "
                )

                schedule_appointment(
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    reason
                )

            except ValueError:

                print("\nPlease enter valid values.")

        elif choice == "2":

            view_appointments()

        elif choice == "3":

            try:

                appointment_id = int(
                    input("Enter appointment ID: ")
                )

                status = input(
                    "Enter status: "
                )

                update_appointment_status(
                    appointment_id,
                    status
                )

            except ValueError:

                print("\nPlease enter a valid appointment ID.")

        elif choice == "4":

            try:

                appointment_id = int(
                    input("Enter appointment ID: ")
                )

                cancel_appointment(
                    appointment_id
                )

            except ValueError:

                print("\nPlease enter a valid appointment ID.")

        elif choice == "5":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                view_patient_appointments(
                    patient_id
                )

            except ValueError:

                print("\nPlease enter a valid patient ID.")

        elif choice == "6":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# BILLING MENU
# ============================================================

def billing_menu():

    while True:

        print("\n========== BILLING MENU ==========")
        print("1. Create bill")
        print("2. View all bills")
        print("3. Update payment status")
        print("4. View patient bills")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                consultation_fee = float(
                    input("Enter consultation fee: ")
                )

                room_charge = float(
                    input("Enter room charge: ")
                )

                laboratory_charge = float(
                    input("Enter laboratory charge: ")
                )

                medicine_charge = float(
                    input("Enter medicine charge: ")
                )

                discount = float(
                    input("Enter discount percentage: ")
                )

                tax_rate = float(
                    input("Enter tax percentage: ")
                )

                create_bill(
                    patient_id=patient_id,
                    consultation_fee=consultation_fee,
                    room_charge=room_charge,
                    laboratory_charge=laboratory_charge,
                    medicine_charge=medicine_charge,
                    discount=discount,
                    tax_rate=tax_rate
                )

            except ValueError:

                print("\nPlease enter valid numeric values.")

        elif choice == "2":

            view_bills()

        elif choice == "3":

            try:

                bill_id = int(
                    input("Enter bill ID: ")
                )

                payment_status = input(
                    "Enter payment status "
                    "(Pending/Paid/Partially Paid/Cancelled): "
                )

                update_payment_status(
                    bill_id,
                    payment_status
                )

            except ValueError:

                print("\nPlease enter a valid bill ID.")

        elif choice == "4":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                view_patient_bills(
                    patient_id
                )

            except ValueError:

                print("\nPlease enter a valid patient ID.")

        elif choice == "5":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# PHARMACY MENU
# ============================================================

def pharmacy_menu():

    while True:

        print("\n========== PHARMACY MENU ==========")
        print("1. Add medicine")
        print("2. View all medicines")
        print("3. Update medicine stock")
        print("4. Check low-stock medicines")
        print("5. Check near-expiry medicines")
        print("6. Check expired medicines")
        print("7. Return to Main Menu")

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # ADD MEDICINE
        # ----------------------------------------------------

        if choice == "1":

            try:

                name = input(
                    "Enter medicine name: "
                )

                manufacturer = input(
                    "Enter manufacturer: "
                )

                price = float(
                    input("Enter price: ")
                )

                stock_quantity = int(
                    input("Enter stock quantity: ")
                )

                expiry_date = input(
                    "Enter expiry date (YYYY-MM-DD): "
                )

                reorder_level = int(
                    input("Enter reorder level: ")
                )

                add_medicine(
                    name,
                    manufacturer,
                    price,
                    stock_quantity,
                    expiry_date,
                    reorder_level
                )

            except ValueError:

                print("\nPlease enter valid numeric values.")

        # ----------------------------------------------------
        # VIEW MEDICINES
        # ----------------------------------------------------

        elif choice == "2":

            view_medicines()

        # ----------------------------------------------------
        # UPDATE STOCK
        # ----------------------------------------------------

        elif choice == "3":

            try:

                medicine_id = int(
                    input("Enter medicine ID: ")
                )

                quantity_change = int(
                    input(
                        "Enter quantity change "
                        "(negative to reduce): "
                    )
                )

                update_medicine_stock(
                    medicine_id,
                    quantity_change
                )

            except ValueError:

                print("\nPlease enter valid numbers.")

        # ----------------------------------------------------
        # LOW STOCK
        # ----------------------------------------------------

        elif choice == "4":

            check_low_stock()

        # ----------------------------------------------------
        # NEAR EXPIRY
        # ----------------------------------------------------

        elif choice == "5":

            try:

                days = int(
                    input("Enter number of days to check: ")
                )

                if days < 0:

                    print(
                        "\nNumber of days cannot be negative."
                    )

                else:

                    check_near_expiry(days)

            except ValueError:

                print("\nPlease enter a valid number.")

        # ----------------------------------------------------
        # EXPIRED MEDICINES
        # ----------------------------------------------------

        elif choice == "6":

            check_expired_medicines()

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "7":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# PATIENT MENU
# ============================================================

def patient_menu():

    while True:

        print("\n========== PATIENT MANAGEMENT ==========")
        print("1. Register new patient")
        print("2. View all patients")
        print("3. Search patient")
        print("4. Update patient")
        print("5. Delete patient")
        print("6. Return to Main Menu")

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # REGISTER PATIENT
        # ----------------------------------------------------

        if choice == "1":

            try:

                first_name = input(
                    "Enter first name: "
                ).strip()

                last_name = input(
                    "Enter last name: "
                ).strip()

                gender = input(
                    "Enter gender: "
                ).strip()

                date_of_birth = input(
                    "Enter date of birth (YYYY-MM-DD): "
                ).strip()

                phone = input(
                    "Enter phone number: "
                ).strip()

                email = input(
                    "Enter email (optional): "
                ).strip()

                address = input(
                    "Enter address (optional): "
                ).strip()

                blood_group = input(
                    "Enter blood group (optional): "
                ).strip()

                emergency_contact = input(
                    "Enter emergency contact (optional): "
                ).strip()

                if not first_name or not last_name:

                    print(
                        "\nFirst name and last name "
                        "cannot be empty."
                    )

                    continue

                register_patient(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    phone=phone,
                    email=email or None,
                    address=address or None,
                    blood_group=blood_group or None,
                    emergency_contact=emergency_contact or None
                )

            except Exception as error:

                print("\nError:", error)

        # ----------------------------------------------------
        # VIEW PATIENTS
        # ----------------------------------------------------

        elif choice == "2":

            view_patients()

        # ----------------------------------------------------
        # SEARCH PATIENT
        # ----------------------------------------------------

        elif choice == "3":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                search_patient(patient_id)

            except ValueError:

                print(
                    "\nPlease enter a valid patient ID."
                )

        # ----------------------------------------------------
        # UPDATE PATIENT
        # ----------------------------------------------------

        elif choice == "4":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                print("\nEnter the new patient details.")

                phone = input(
                    "Enter new phone number: "
                ).strip()

                email = input(
                    "Enter new email: "
                ).strip()

                address = input(
                    "Enter new address: "
                ).strip()

                blood_group = input(
                    "Enter new blood group: "
                ).strip()

                emergency_contact = input(
                    "Enter new emergency contact: "
                ).strip()

                update_patient(
                    patient_id=patient_id,
                    phone=phone or None,
                    email=email or None,
                    address=address or None,
                    blood_group=blood_group or None,
                    emergency_contact=emergency_contact or None
                )

            except ValueError:

                print(
                    "\nPlease enter a valid patient ID."
                )

        # ----------------------------------------------------
        # DELETE PATIENT
        # ----------------------------------------------------

        elif choice == "5":

            try:

                patient_id = int(
                    input("Enter patient ID to delete: ")
                )

                confirmation = input(
                    "Are you sure you want to delete "
                    "this patient? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":

                    delete_patient(patient_id)

                else:

                    print("\nPatient deletion cancelled.")

            except ValueError:

                print(
                    "\nPlease enter a valid patient ID."
                )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "6":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# DOCTOR MENU
# ============================================================

def doctor_menu():

    while True:

        print("\n========== DOCTOR MANAGEMENT ==========")
        print("1. Add doctor")
        print("2. View all doctors")
        print("3. Search doctor")
        print("4. Return to Main Menu")

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # ADD DOCTOR
        # ----------------------------------------------------

        if choice == "1":

            try:

                first_name = input(
                    "Enter first name: "
                ).strip()

                last_name = input(
                    "Enter last name: "
                ).strip()

                gender = input(
                    "Enter gender: "
                ).strip()

                phone = input(
                    "Enter phone number: "
                ).strip()

                email = input(
                    "Enter email (optional): "
                ).strip()

                specialization = input(
                    "Enter specialization: "
                ).strip()

                department_id = int(
                    input("Enter department ID: ")
                )

                consultation_fee = float(
                    input("Enter consultation fee: ")
                )

                if not first_name or not last_name:

                    print(
                        "\nFirst name and last name "
                        "cannot be empty."
                    )

                    continue

                if consultation_fee < 0:

                    print(
                        "\nConsultation fee cannot be negative."
                    )

                    continue

                add_doctor(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    phone=phone,
                    specialization=specialization,
                    department_id=department_id,
                    consultation_fee=consultation_fee,
                    email=email or None
                )

            except ValueError:

                print(
                    "\nPlease enter valid numeric values "
                    "for department ID and consultation fee."
                )

        # ----------------------------------------------------
        # VIEW DOCTORS
        # ----------------------------------------------------

        elif choice == "2":

            view_doctors()

        # ----------------------------------------------------
        # SEARCH DOCTOR
        # ----------------------------------------------------

        elif choice == "3":

            try:

                doctor_id = int(
                    input("Enter doctor ID: ")
                )

                search_doctor(doctor_id)

            except ValueError:

                print(
                    "\nPlease enter a valid doctor ID."
                )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "4":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# STAFF MENU
# ============================================================

def staff_menu():

    while True:

        print("\n========== STAFF MANAGEMENT ==========")
        print("1. Add staff member")
        print("2. View all staff")
        print("3. Search staff by job")
        print("4. Delete staff member")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # ADD STAFF
        # ----------------------------------------------------

        if choice == "1":

            try:

                first_name = input(
                    "Enter first name: "
                ).strip()

                last_name = input(
                    "Enter last name: "
                ).strip()

                gender = input(
                    "Enter gender: "
                ).strip()

                phone = input(
                    "Enter phone number: "
                ).strip()

                email = input(
                    "Enter email: "
                ).strip()

                job_title = input(
                    "Enter job title: "
                ).strip()

                salary = float(
                    input("Enter salary: ")
                )

                if not first_name or not last_name:

                    print(
                        "\nFirst name and last name "
                        "cannot be empty."
                    )

                    continue

                add_staff(
                    first_name,
                    last_name,
                    gender,
                    phone,
                    email,
                    job_title,
                    salary
                )

            except ValueError:

                print("\nPlease enter a valid salary.")

        # ----------------------------------------------------
        # VIEW STAFF
        # ----------------------------------------------------

        elif choice == "2":

            view_staff()

        # ----------------------------------------------------
        # SEARCH STAFF
        # ----------------------------------------------------

        elif choice == "3":

            job_title = input(
                "Enter job title to search: "
            ).strip()

            if not job_title:

                print("\nPlease enter a job title.")

            else:

                search_staff_by_job(
                    job_title
                )

        # ----------------------------------------------------
        # DELETE STAFF
        # ----------------------------------------------------

        elif choice == "4":

            try:

                staff_id = int(
                    input("Enter staff ID to delete: ")
                )

                delete_staff(
                    staff_id
                )

            except ValueError:

                print(
                    "\nPlease enter a valid staff ID."
                )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "5":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# ROOM & ADMISSION MENU
# ============================================================

def room_admission_menu():

    while True:

        print("\n========== ROOM & ADMISSION MENU ==========")
        print("1. Add room")
        print("2. View all rooms")
        print("3. View available rooms")
        print("4. Admit patient manually")
        print("5. Auto allocate room & admit patient")
        print("6. View current admissions")
        print("7. Discharge patient")
        print("8. View patient admission history")
        print("9. Return to Main Menu")

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # ADD ROOM
        # ----------------------------------------------------

        if choice == "1":

            try:

                room_number = input(
                    "Enter room number: "
                ).strip()

                room_type = input(
                    "Enter room type: "
                ).strip()

                daily_charge = float(
                    input("Enter daily charge: ")
                )

                add_room(
                    room_number,
                    room_type,
                    daily_charge
                )

            except ValueError:

                print(
                    "\nPlease enter a valid daily charge."
                )

        # ----------------------------------------------------
        # VIEW ALL ROOMS
        # ----------------------------------------------------

        elif choice == "2":

            view_rooms()

        # ----------------------------------------------------
        # VIEW AVAILABLE ROOMS
        # ----------------------------------------------------

        elif choice == "3":

            view_available_rooms()

        # ----------------------------------------------------
        # MANUAL ADMISSION
        # ----------------------------------------------------

        elif choice == "4":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                room_id = int(
                    input("Enter room ID: ")
                )

                doctor_input = input(
                    "Enter doctor ID "
                    "(press Enter if none): "
                ).strip()

                doctor_id = (
                    int(doctor_input)
                    if doctor_input
                    else None
                )

                diagnosis = input(
                    "Enter diagnosis: "
                ).strip()

                admit_patient(
                    patient_id,
                    room_id,
                    doctor_id,
                    diagnosis or None
                )

            except ValueError:

                print(
                    "\nPlease enter valid numeric values."
                )

        # ----------------------------------------------------
        # AUTOMATIC ROOM ALLOCATION
        # ----------------------------------------------------

        elif choice == "5":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                doctor_input = input(
                    "Enter doctor ID "
                    "(press Enter if none): "
                ).strip()

                doctor_id = (
                    int(doctor_input)
                    if doctor_input
                    else None
                )

                diagnosis = input(
                    "Enter diagnosis: "
                ).strip()

                room_type = input(
                    "Enter preferred room type "
                    "(press Enter for any room): "
                ).strip()

                auto_allocate_room(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    diagnosis=diagnosis or None,
                    room_type=room_type or None
                )

            except ValueError:

                print(
                    "\nPlease enter valid numeric values."
                )

        # ----------------------------------------------------
        # CURRENT ADMISSIONS
        # ----------------------------------------------------

        elif choice == "6":

            view_current_admissions()

        # ----------------------------------------------------
        # DISCHARGE
        # ----------------------------------------------------

        elif choice == "7":

            try:

                admission_id = int(
                    input("Enter admission ID: ")
                )

                discharge_patient(
                    admission_id
                )

            except ValueError:

                print(
                    "\nPlease enter a valid admission ID."
                )

        # ----------------------------------------------------
        # PATIENT ADMISSION HISTORY
        # ----------------------------------------------------

        elif choice == "8":

            try:

                patient_id = int(
                    input("Enter patient ID: ")
                )

                view_patient_admissions(
                    patient_id
                )

            except ValueError:

                print(
                    "\nPlease enter a valid patient ID."
                )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "9":

            print("\nReturning to Main Menu...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    # Create database tables
    create_tables()

    while True:

        print("\n")
        print("==============================================")
        print("       HOSPITAL MANAGEMENT SYSTEM")
        print("==============================================")

        print("1. Dashboard")
        print("2. Patient Management")
        print("3. Doctor Management")
        print("4. Appointment Management")
        print("5. Medical History")
        print("6. Laboratory Tests")
        print("7. Billing")
        print("8. Pharmacy")
        print("9. Staff Management")
        print("10. Room & Admission Management")
        print("11. Reports")
        print("12. Exit")

        print("==============================================")

        choice = input(
            "Enter your choice: "
        ).strip()

        # ----------------------------------------------------
        # DASHBOARD
        # ----------------------------------------------------

        if choice == "1":

            show_dashboard()

        # ----------------------------------------------------
        # PATIENT
        # ----------------------------------------------------

        elif choice == "2":

            patient_menu()

        # ----------------------------------------------------
        # DOCTOR
        # ----------------------------------------------------

        elif choice == "3":

            doctor_menu()

        # ----------------------------------------------------
        # APPOINTMENT
        # ----------------------------------------------------

        elif choice == "4":

            appointment_menu()

        # ----------------------------------------------------
        # MEDICAL HISTORY
        # ----------------------------------------------------

        elif choice == "5":

            medical_history_menu()

        # ----------------------------------------------------
        # LABORATORY
        # ----------------------------------------------------

        elif choice == "6":

            laboratory_menu()

        # ----------------------------------------------------
        # BILLING
        # ----------------------------------------------------

        elif choice == "7":

            billing_menu()

        # ----------------------------------------------------
        # PHARMACY
        # ----------------------------------------------------

        elif choice == "8":

            pharmacy_menu()

        # ----------------------------------------------------
        # STAFF
        # ----------------------------------------------------

        elif choice == "9":

            staff_menu()

        # ----------------------------------------------------
        # ROOM & ADMISSION
        # ----------------------------------------------------

        elif choice == "10":

            room_admission_menu()

        # ----------------------------------------------------
        # REPORTS
        # ----------------------------------------------------

        elif choice == "11":

            report_menu()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "12":

            print("\nThank you for using")
            print("Hospital Management System.")
            print("Goodbye!")

            break

        # ----------------------------------------------------
        # INVALID CHOICE
        # ----------------------------------------------------

        else:

            print(
                "\nInvalid choice. "
                "Please enter a number from 1 to 12."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
