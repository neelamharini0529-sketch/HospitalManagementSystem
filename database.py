import sqlite3


DATABASE_NAME = "hospital.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(DATABASE_NAME)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create all tables required for the Hospital Management System."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==========================================
        # DEPARTMENTS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        """)


        # ==========================================
        # PATIENTS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                blood_group TEXT,
                emergency_contact TEXT,
                registration_date TEXT NOT NULL
            )
        """)


        # ==========================================
        # DOCTORS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                specialization TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                consultation_fee REAL NOT NULL,

                FOREIGN KEY (department_id)
                    REFERENCES departments(department_id)
            )
        """)


        # ==========================================
        # STAFF TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT,
                phone TEXT,
                email TEXT,
                job_title TEXT,
                salary REAL
            )
        """)


        # ==========================================
        # APPOINTMENTS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'Scheduled',

                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id),

                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(doctor_id)
            )
        """)


        # ==========================================
        # ROOMS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT NOT NULL UNIQUE,
                room_type TEXT NOT NULL,
                daily_charge REAL NOT NULL,
                status TEXT DEFAULT 'Available'
            )
        """)


        # ==========================================
        # ADMISSIONS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admissions (
                admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                doctor_id INTEGER,
                admission_date TEXT NOT NULL,
                discharge_date TEXT,
                diagnosis TEXT,
                status TEXT DEFAULT 'Admitted',

                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id),

                FOREIGN KEY (room_id)
                    REFERENCES rooms(room_id),

                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(doctor_id)
            )
        """)


        # ==========================================
        # MEDICAL HISTORY TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER,
                record_date TEXT NOT NULL,
                diagnosis TEXT,
                treatment TEXT,
                allergies TEXT,
                notes TEXT,

                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id),

                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(doctor_id)
            )
        """)

        # ==========================================
        # LABORATORY TESTS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS laboratory_tests (
                test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER,
                test_name TEXT NOT NULL,
                test_date TEXT NOT NULL,
                result TEXT,
                status TEXT DEFAULT 'Pending',
                notes TEXT,

                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id),

                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(doctor_id)
            )
        """)

        # ==========================================
        # BILLS TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                consultation_fee REAL DEFAULT 0,
                room_charge REAL DEFAULT 0,
                laboratory_charge REAL DEFAULT 0,
                medicine_charge REAL DEFAULT 0,
                subtotal REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                tax_rate REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total_amount REAL DEFAULT 0,
                payment_status TEXT DEFAULT 'Pending',
                bill_date TEXT NOT NULL,

                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id)
            )
        """)


        # ==========================================
        # MEDICINES TABLE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                manufacturer TEXT,
                price REAL NOT NULL,
                stock_quantity INTEGER NOT NULL,
                expiry_date TEXT NOT NULL,
                reorder_level INTEGER DEFAULT 10
            )
        """)


        # ==========================================
        # COMMIT CHANGES
        # ==========================================

        connection.commit()

        print("\nAll database tables created successfully!")

    except sqlite3.Error as error:

        connection.rollback()

        print("\nDatabase error:", error)

    finally:

        connection.close()


# ==========================================
# RUN DATABASE SETUP
# ==========================================

if __name__ == "__main__":
    create_tables()