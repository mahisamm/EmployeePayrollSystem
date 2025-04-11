import sqlite3
from datetime import datetime

def create_tables():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        basic_salary REAL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        emp_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salary (
        emp_id INTEGER,
        month TEXT,
        working_days INTEGER,
        basic_salary REAL,
        tax REAL,
        net_salary REAL,
        FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
    )''')
    conn.commit()
    conn.close()

def add_employee():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    name = input("Enter employee name: ")
    position = input("Enter position: ")
    salary = float(input("Enter basic salary: "))
    cursor.execute("INSERT INTO employees (name, position, basic_salary) VALUES (?, ?, ?)",
                    (name, position, salary))
    conn.commit()
    conn.close()
    print("Employee added successfully.")

def view_employees():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    print("\n--- Employee List ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Basic Salary: {row[3]}")
    conn.close()

def mark_attendance():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    emp_id = int(input("Enter employee ID: "))
    status = input("Enter status (Present/Absent): ")
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO attendance (emp_id, date, status) VALUES (?, ?, ?)",
                    (emp_id, date, status.capitalize()))
    conn.commit()
    conn.close()
    print("Attendance marked.")

def calculate_salary():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    emp_id = int(input("Enter employee ID: "))
    month = input("Enter month (e.g., April 2025): ")
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE emp_id = ? AND status = 'Present'", (emp_id,))
    working_days = cursor.fetchone()[0]
    cursor.execute("SELECT basic_salary FROM employees WHERE emp_id = ?", (emp_id,))
    result = cursor.fetchone()
    if result:
        basic_salary = result[0]
        tax = 0.1 * basic_salary
        net_salary = (basic_salary * working_days / 30) - tax
        cursor.execute("INSERT INTO salary (emp_id, month, working_days, basic_salary, tax, net_salary) VALUES (?, ?, ?, ?, ?, ?)",
                        (emp_id, month, working_days, basic_salary, tax, net_salary))
        conn.commit()
        print("Salary calculated and recorded.")
    else:
        print("Employee not found.")
    conn.close()

def generate_report():
    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()
    emp_id = int(input("Enter employee ID: "))
    cursor.execute("SELECT * FROM salary WHERE emp_id = ?", (emp_id,))
    records = cursor.fetchall()
    print("\n--- Payroll Report ---")
    for rec in records:
        print(f"Month: {rec[1]}, Working Days: {rec[2]}, Basic: {rec[3]}, Tax: {rec[4]}, Net Salary: {rec[5]}")
    conn.close()

def main_menu():
    create_tables()
    while True:
        print("\n=== Employee Payroll Management System ===")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Mark Attendance")
        print("4. Calculate Salary")
        print("5. Generate Payroll Report")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_employee()
        elif choice == '2':
            view_employees()
        elif choice == '3':
            mark_attendance()
        elif choice == '4':
            calculate_salary()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            print("Exiting system...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()