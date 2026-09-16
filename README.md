# Hospital Management System

A complete **Hospital Management System** developed using **Python and SQLite**. The system manages patients, doctors, appointments, medical records, laboratory tests, pharmacy, billing, staff, rooms, admissions, and reports through a menu-driven application.

## Project Overview

The Hospital Management System is designed to manage the major administrative and operational activities of a hospital.

The application uses **Python for the application logic** and **SQLite for database management**. It demonstrates practical Python programming concepts including object-oriented programming, functions, modules, exception handling, validation, date/time handling, and relational database operations.

## Features

### Patient Management

* Register patients
* Store patient personal information
* Blood group and emergency contact details
* View patient records

### Doctor Management

* Add doctors
* Assign doctors to departments
* Store consultation fees
* View doctor information

### Department Management

* Create departments
* Store department descriptions
* Associate doctors with departments

### Appointment Management

* Schedule appointments
* View appointments
* Cancel appointments
* Complete appointments
* Prevent doctor double-booking for the same date and time

### Medical History

* Record patient diagnosis
* Store treatment information
* Record allergies
* Add medical notes
* View complete medical history

### Laboratory Management

* Create laboratory test records
* Associate tests with patients and doctors
* Store test results
* Track test status
* View laboratory reports

### Pharmacy Management

* Add medicines
* Track medicine price
* Track stock quantity
* Store expiry dates
* Set reorder levels
* Update medicine stock
* Detect low-stock medicines
* Detect expired medicines
* Detect medicines approaching expiry

### Billing Management

* Create patient bills
* Calculate subtotal
* Apply discounts
* Calculate tax
* Calculate final bill amount
* Track payment status
* View patient bills
* Generate revenue summaries

### Staff Management

* Add hospital staff
* Store job titles
* Store salary information
* View staff records

### Room & Admission Management

* Add hospital rooms
* Track room types
* Track room charges
* View available rooms
* Admit patients
* Automatically allocate available rooms
* Discharge patients
* View current admissions
* View patient admission history

### Reports

The system provides reports for:

* Patients
* Doctors
* Appointments
* Admissions
* Pharmacy stock
* Expired medicines
* Laboratory tests
* Billing and revenue
* Staff
* Complete patient transaction history

### Dashboard

The dashboard provides a quick overview of:

* Total patients
* Total doctors
* Total staff
* Total appointments
* Currently admitted patients
* Total medicines
* Low-stock medicines
* Pending bills
* Paid revenue

## Challenging Features

The project implements several practical hospital-management features:

### Doctor Double-Booking Prevention

The system checks whether a doctor already has an active appointment at the requested date and time.

If the doctor is already booked, the new appointment is rejected.

### Automatic Room Allocation

The system can automatically find an available room and allocate it to a patient during admission.

### Medicine Stock Monitoring

The pharmacy module compares current stock with the configured reorder level and identifies medicines that require restocking.

### Medicine Expiry Monitoring

The system identifies expired medicines and can detect medicines approaching their expiry date.

### Automatic Bill Calculation

The billing system calculates:

```text
Subtotal
- Discount
+ Tax
= Final Bill Amount
```

### Patient Transaction History

A patient's transaction history combines information from multiple hospital modules, including:

* Appointments
* Medical history
* Laboratory tests
* Admissions
* Bills

## Technologies Used

* **Python 3**
* **SQLite**
* **SQL**
* **Object-Oriented Programming**
* **VS Code**
* **Git / GitHub**

## Python Concepts Demonstrated

This project demonstrates:

* Variables and data types
* Conditional statements
* Loops
* Functions
* Modules and packages
* Object-Oriented Programming
* Classes and objects
* Inheritance
* Encapsulation
* Exception handling
* Input validation
* Date and time handling
* File handling
* SQLite database connectivity
* SQL queries
* Primary keys
* Foreign keys
* Relationships between database tables
* CRUD operations
* Menu-driven programming

## Project Structure

```text
HospitalManagementSystem/
│
├── database.py
├── main.py
├── README.md
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── admission.py
│   ├── appointment.py
│   ├── billing.py
│   ├── department.py
│   ├── doctor.py
│   ├── laboratory_test.py
│   ├── medical_history.py
│   ├── patient.py
│   ├── person.py
│   ├── pharmacy.py
│   ├── room.py
│   └── staff.py
│
├── services/
│   ├── __init__.py
│   ├── admission_service.py
│   ├── appointment_service.py
│   ├── billing_service.py
│   ├── dashboard_service.py
│   ├── department_service.py
│   ├── doctor_service.py
│   ├── laboratory_service.py
│   ├── medical_history_service.py
│   ├── patient_history_service.py
│   ├── patient_service.py
│   ├── pharmacy_service.py
│   ├── report_service.py
│   ├── room_service.py
│   └── staff_service.py
│
├── utils/
│   └── __init__.py
│
└── venv/
```

## Database

The application uses **SQLite** through Python's built-in `sqlite3` module.

The database contains related tables for the different hospital modules.

Foreign-key constraints are enabled to maintain relationships between records.

The database file is:

```text
hospital.db
```

## How to Run

### 1. Open the project

Open the project folder in VS Code.

### 2. Activate the virtual environment

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Run the application

```bash
python3 main.py
```

### 4. Use the menu

The main menu provides access to all hospital management modules.

## Example Dashboard

```text
================================================
          HOSPITAL DASHBOARD
================================================

Total Patients       : 1
Total Doctors        : 2
Total Staff          : 1
Total Appointments   : 4
Currently Admitted   : 0
Total Medicines      : 6

---------------- ALERTS ----------------
Low Stock Medicines  : 2
Pending Bills        : 1

---------------- FINANCE ----------------
Total Paid Revenue   : ₹2415.00

================================================
```

## Testing

The following functionality has been tested successfully:

* Patient management
* Doctor management
* Department management
* Appointment scheduling
* Double-booking prevention
* Medical history
* Laboratory tests
* Billing
* Pharmacy stock management
* Low-stock detection
* Expired medicine detection
* Staff management
* Room management
* Automatic room allocation
* Patient admission
* Patient discharge
* Admission history
* Reports
* Patient transaction history
* Dashboard
* Application startup and shutdown

## Future Enhancements

Possible future improvements include:

* Graphical user interface
* Web-based interface
* User authentication and role-based access
* PDF invoice generation
* Email/SMS appointment notifications
* Online appointment booking
* Advanced analytics and charts
* Database backup and restore
* Prescription management
* Insurance management

## Author

**Hospital Management System Project**

Developed using Python and SQLite as a practical software development project.
