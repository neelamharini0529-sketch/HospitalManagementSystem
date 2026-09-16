from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "hospital.db"


# ============================================================
# DASHBOARD DATA
# ============================================================

def get_dashboard_data():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM admissions
            WHERE status = 'Admitted'
        """)
        current_admissions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM bills
            WHERE payment_status = 'Pending'
        """)
        pending_bills = cursor.fetchone()[0]

        return {
            "patients": total_patients,
            "doctors": total_doctors,
            "appointments": total_appointments,
            "admissions": current_admissions,
            "medicines": total_medicines,
            "pending_bills": pending_bills
        }

    finally:
        connection.close()


# ============================================================
# HOME / DASHBOARD
# ============================================================

@app.route("/")
def home():

    dashboard = get_dashboard_data()

    return render_template(
        "dashboard.html",
        dashboard=dashboard
    )


# ============================================================
# PATIENTS
# ============================================================

@app.route("/patients")
def patients():

    connection = sqlite3.connect(DATABASE)
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
                blood_group
            FROM patients
            ORDER BY patient_id
        """)

        patients_data = cursor.fetchall()

        return render_template(
            "patients.html",
            patients=patients_data
        )

    finally:
        connection.close()


# ============================================================
# DOCTORS
# ============================================================

@app.route("/doctors")
def doctors():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                doctor_id,
                first_name,
                last_name,
                gender,
                phone,
                email,
                specialization,
                department_id,
                consultation_fee
            FROM doctors
            ORDER BY doctor_id
        """)

        doctors_data = cursor.fetchall()

        return render_template(
            "doctors.html",
            doctors=doctors_data
        )

    finally:
        connection.close()



# ============================================================
# APPOINTMENTS
# ============================================================

@app.route("/appointments")
def appointments():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                a.appointment_id,
                p.first_name || ' ' || p.last_name AS patient_name,
                d.first_name || ' ' || d.last_name AS doctor_name,
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

        appointments_data = cursor.fetchall()

        return render_template(
            "appointments.html",
            appointments=appointments_data
        )

    finally:
        connection.close()

# ============================================================
# MEDICAL HISTORY
# ============================================================

@app.route("/medical-history")
def medical_history():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                mh.history_id,
                p.first_name || ' ' || p.last_name AS patient_name,
                d.first_name || ' ' || d.last_name AS doctor_name,
                mh.record_date,
                mh.diagnosis,
                mh.treatment,
                mh.allergies,
                mh.notes
            FROM medical_history mh
            JOIN patients p
                ON mh.patient_id = p.patient_id
            JOIN doctors d
                ON mh.doctor_id = d.doctor_id
            ORDER BY mh.record_date DESC
        """)

        history_data = cursor.fetchall()

        return render_template(
            "medical_history.html",
            medical_history=history_data
        )

    finally:
        connection.close()


# ============================================================
# LABORATORY
# ============================================================

@app.route("/laboratory")
def laboratory():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                lt.test_id,
                p.first_name || ' ' || p.last_name AS patient_name,
                d.first_name || ' ' || d.last_name AS doctor_name,
                lt.test_name,
                lt.test_date,
                lt.result,
                lt.status
            FROM laboratory_tests lt
            JOIN patients p
                ON lt.patient_id = p.patient_id
            LEFT JOIN doctors d
                ON lt.doctor_id = d.doctor_id
            ORDER BY lt.test_date DESC
        """)

        laboratory_data = cursor.fetchall()

        return render_template(
            "laboratory.html",
            laboratory_tests=laboratory_data
        )

    finally:
        connection.close()

# ============================================================
# PHARMACY
# ============================================================

@app.route("/pharmacy")
def pharmacy():

    connection = sqlite3.connect(DATABASE)
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

        medicines_data = cursor.fetchall()

        pharmacy_data = []

        from datetime import date

        today = date.today()

        for medicine in medicines_data:

            expiry_date = medicine[5]
            stock_quantity = medicine[4]
            reorder_level = medicine[6]

            try:
                expiry = date.fromisoformat(expiry_date)

                if expiry < today:
                    status = "Expired"

                elif stock_quantity <= reorder_level:
                    status = "Low Stock"

                else:
                    status = "Available"

            except ValueError:
                status = "Available"

            pharmacy_data.append(
                medicine + (status,)
            )

        return render_template(
            "pharmacy.html",
            medicines=pharmacy_data
        )

    finally:
        connection.close()

# ============================================================
# BILLING
# ============================================================

@app.route("/billing")
def billing():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                b.bill_id,
                p.first_name || ' ' || p.last_name AS patient_name,
                b.consultation_fee,
                b.room_charge,
                b.laboratory_charge,
                b.medicine_charge,
                b.discount_amount,
                b.tax_amount,
                b.total_amount,
                b.payment_status,
                b.bill_date
            FROM bills b
            JOIN patients p
                ON b.patient_id = p.patient_id
            ORDER BY b.bill_date DESC, b.bill_id DESC
        """)

        bills_data = cursor.fetchall()

        return render_template(
            "billing.html",
            bills=bills_data
        )

    finally:
        connection.close()


# ============================================================
# STAFF
# ============================================================

@app.route("/staff")
def staff():

    connection = sqlite3.connect(DATABASE)
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

        staff_data = cursor.fetchall()

        print("STAFF DATA:", staff_data)

        return render_template(
            "staff.html",
            staff=staff_data
        )

    except Exception as e: 
        print("STAFF ERROR:", e) 
        return f"Staff error: {e}"

    finally:
        connection.close()


# ============================================================
# ROOMS
# ============================================================

@app.route("/rooms")
def rooms():

    connection = sqlite3.connect(DATABASE)
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

        rooms_data = cursor.fetchall()

        print("ROOM DATA:", rooms_data)

        return render_template(
            "rooms.html",
            rooms=rooms_data
        )

    finally:
        connection.close()


# ============================================================
# REPORTS
# ============================================================

@app.route("/reports")
def reports():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        # Total patients
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        # Total doctors
        cursor.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = cursor.fetchone()[0]

        # Total appointments
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cursor.fetchone()[0]

        # Current admissions
        cursor.execute("""
            SELECT COUNT(*)
            FROM admissions
            WHERE status = 'Admitted'
        """)
        total_admissions = cursor.fetchone()[0]

        # Total medicines
        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        # Total staff
        cursor.execute("SELECT COUNT(*) FROM staff")
        total_staff = cursor.fetchone()[0]

        # Total rooms
        cursor.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = cursor.fetchone()[0]

        # Pending bills
        cursor.execute("""
            SELECT COUNT(*)
            FROM bills
            WHERE payment_status = 'Pending'
        """)
        pending_bills = cursor.fetchone()[0]

        # Paid revenue
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM bills
            WHERE payment_status = 'Paid'
        """)
        revenue = cursor.fetchone()[0]

        reports_data = {
            "patients": total_patients,
            "doctors": total_doctors,
            "appointments": total_appointments,
            "admissions": total_admissions,
            "medicines": total_medicines,
            "staff": total_staff,
            "rooms": total_rooms,
            "pending_bills": pending_bills,
            "revenue": revenue
        }

        return render_template(
            "reports.html",
            reports=reports_data
        )

    finally:
        connection.close()


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)