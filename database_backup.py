
import sqlite3
import os
import shutil
from datetime import datetime

DATABASE = "company.db"
BACKUP_FOLDER = "database_backups"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_employee():
    name = input("Enter employee name: ").strip()
    department = input("Enter department: ").strip()

    try:
        salary = float(input("Enter salary: "))

        if not name or not department or salary <= 0:
            print("Invalid employee details!")
            return

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            (name, department, salary)
        )

        connection.commit()
        connection.close()

        print("Employee added successfully!")

    except ValueError:
        print("Salary must be a valid number.")


def view_employees():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees")

    records = cursor.fetchall()

    connection.close()

    print("\n===== EMPLOYEE RECORDS =====")

    if not records:
        print("No employees found.")
        return

    for record in records:
        print(record)


def create_backup():
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_file = os.path.join(
        BACKUP_FOLDER,
        f"company_backup_{timestamp}.db"
    )

    source = sqlite3.connect(DATABASE)
    destination = sqlite3.connect(backup_file)

    try:
        source.backup(destination)
        print("\nBackup created successfully!")
        print("Location:", backup_file)

    finally:
        destination.close()
        source.close()


def view_backups():
    if not os.path.exists(BACKUP_FOLDER):
        print("No backups found.")
        return

    backups = sorted(os.listdir(BACKUP_FOLDER))

    print("\n===== AVAILABLE BACKUPS =====")

    if not backups:
        print("No backups available.")
        return

    for index, file in enumerate(backups, start=1):
        print(index, file)


def main():
    create_database()

    while True:
        print("\n===== DATABASE BACKUP MANAGER =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Create Database Backup")
        print("4. View Backups")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            create_backup()

        elif choice == "4":
            view_backups()

        elif choice == "5":
            print("Exiting Backup Manager...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
