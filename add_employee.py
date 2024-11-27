import csv
import os

def add_employee():
    # Define the CSV file name
    filename = 'employee_data.csv'
    
    # Check if the CSV file exists; if not, create it with headers
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['rfid_id', 'employee_name', 'department', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
    # Collect employee information
    print("\n--- Add New Employee ---")
    rfid_id = input("Enter RFID ID: ").strip()
    employee_name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()
    email = input("Enter Email: ").strip()
    
    # Validate inputs
    if not rfid_id or not employee_name or not department or not email:
        print("All fields are required. Please try again.")
        return
    
    # Check for duplicate RFID IDs
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['rfid_id'] == rfid_id:
                print(f"RFID ID {rfid_id} already exists. Please use a unique RFID ID.")
                return
    
    # Append the new employee to the CSV file
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['rfid_id', 'employee_name', 'department', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'rfid_id': rfid_id,
            'employee_name': employee_name,
            'department': department,
            'email': email
        })
    
    print(f"Employee {employee_name} added successfully with RFID ID {rfid_id}.")

if __name__ == '__main__':
    add_employee()