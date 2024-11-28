import csv
from datetime import datetime
import os

def receive_rfid_data():
    rfid_id = input("Enter RFID ID (simulated scan, or '0000000000' to exit): ").strip()
    print(f"Received RFID ID: {rfid_id}")
    return rfid_id

def get_employee_data(rfid_id):
    employee_data = {}
    try:
        with open('employee_data.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['rfid_id'] == rfid_id:
                    employee_data = row
                    break
            if employee_data:
                print(f"RFID: {employee_data['rfid_id']}")
                print(f"Employee Name: {employee_data['employee_name']}")
                print(f"Department: {employee_data['department']}")
            else:
                print(f"No employee found for RFID ID: {rfid_id}")
            return employee_data
    except FileNotFoundError:
        print("Employee data file not found.")
        return None

def load_food_items():
    food_items = {}
    if not os.path.isfile('food_items.csv'):
        print("Food items file not found.")
        return food_items
    with open('food_items.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_items[row['item_name'].lower()] = row
    return food_items

def capture_items(food_items):
    # Simulate item capture and validation
    print("Enter items on the tray, separated by commas.")
    print("Available items:", ', '.join(food_items.keys()))
    items_input = input("Items: ")
    entered_items = [item.strip().lower() for item in items_input.split(',')]
    valid_items = []
    invalid_items = []
    for item in entered_items:
        if item in food_items:
            valid_items.append(food_items[item])
        else:
            invalid_items.append(item)
    if invalid_items:
        print(f"Invalid items: {', '.join(invalid_items)}")
        print("Please enter valid items from the available list.")
        return None
    return valid_items

def get_new_transaction_id():
    filename = 'transaction_id.txt'
    if not os.path.isfile(filename):
        transaction_id = '0000000000'
    else:
        with open(filename, 'r') as f:
            last_id = f.read().strip()
            if last_id == '':
                transaction_id = '0000000000'
            else:
                new_id = int(last_id) + 1
                transaction_id = str(new_id).zfill(10)

    # Update the transaction ID file with the new ID
    with open(filename, 'w') as f:
        f.write(transaction_id)

    return transaction_id

def log_transaction(transaction):
    # Append the transaction to the transactions CSV file
    filename = 'transactions.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['transaction_id', 'timestamp', 'employee_id', 'employee_name', 'transaction_type', 'items', 'amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)

def calculate_outstanding_balance(employee_id):
    filename = 'transactions.csv'
    if not os.path.isfile(filename):
        return 0.0
    total_purchases = 0.0
    total_payments = 0.0
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['employee_id'] == employee_id:
                if row['transaction_type'] == 'Purchase':
                    total_purchases += float(row['amount'])
                elif row['transaction_type'] == 'Payment':
                    total_payments += float(row['amount'])
    outstanding_balance = total_purchases - total_payments
    return outstanding_balance

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add User")
        print("2. Remove User")
        print("3. Modify User")
        print("4. List All Users")
        print("5. Add Food Item")
        print("6. Remove Food Item")
        print("7. Modify Food Item")
        print("8. List All Food Items")
        print("9. Exit Admin Menu")
        choice = input("Select an option (1-9): ").strip()
        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_employee()
        elif choice == '3':
            modify_employee()
        elif choice == '4':
            list_all_users()
        elif choice == '5':
            add_food_item()
        elif choice == '6':
            remove_food_item()
        elif choice == '7':
            modify_food_item()
        elif choice == '8':
            list_all_food_items()
        elif choice == '9':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid selection. Please try again.")

def add_employee():
    filename = 'employee_data.csv'
    print("\n--- Add New Employee ---")
    rfid_id = input("Enter RFID ID: ").strip()
    employee_name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()
    email = input("Enter Email: ").strip()
    role = input("Enter Role (admin/user): ").strip().lower()
    if role not in ['admin', 'user']:
        print("Invalid role. Defaulting to 'user'.")
        role = 'user'
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
        fieldnames = ['rfid_id', 'employee_name', 'department', 'email', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'rfid_id': rfid_id,
            'employee_name': employee_name,
            'department': department,
            'email': email,
            'role': role
        })
    print(f"Employee {employee_name} added successfully with RFID ID {rfid_id}.")

def remove_employee():
    filename = 'employee_data.csv'
    print("\n--- Remove Employee ---")
    rfid_id = input("Enter RFID ID of the employee to remove: ").strip()
    employees = []
    found = False
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['rfid_id'] != rfid_id:
                employees.append(row)
            else:
                found = True
    if not found:
        print(f"No employee found with RFID ID {rfid_id}.")
        return
    # Write updated list back to CSV
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['rfid_id', 'employee_name', 'department', 'email', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)
    print(f"Employee with RFID ID {rfid_id} removed successfully.")

def modify_employee():
    filename = 'employee_data.csv'
    print("\n--- Modify Employee ---")
    rfid_id = input("Enter RFID ID of the employee to modify: ").strip()
    employees = []
    found = False
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['rfid_id'] == rfid_id:
                found = True
                print(f"Current Data: {row}")
                employee_name = input("Enter new Employee Name (leave blank to keep current): ").strip() or row['employee_name']
                department = input("Enter new Department (leave blank to keep current): ").strip() or row['department']
                email = input("Enter new Email (leave blank to keep current): ").strip() or row['email']
                role = input("Enter new Role (admin/user, leave blank to keep current): ").strip().lower() or row['role']
                if role not in ['admin', 'user']:
                    print("Invalid role. Keeping current role.")
                    role = row['role']
                row.update({
                    'employee_name': employee_name,
                    'department': department,
                    'email': email,
                    'role': role
                })
            employees.append(row)
    if not found:
        print(f"No employee found with RFID ID {rfid_id}.")
        return
    # Write updated list back to CSV
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['rfid_id', 'employee_name', 'department', 'email', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)
    print(f"Employee with RFID ID {rfid_id} modified successfully.")

def list_all_users():
    filename = 'employee_data.csv'
    print("\n--- List of All Employees ---")
    try:
        with open(filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            employees = [row for row in reader]
            if employees:
                headers = ['rfid_id', 'employee_name', 'department', 'email', 'role']
                # If using tabulate
                # print(tabulate(employees, headers=headers, tablefmt='grid'))
                # If not using tabulate, use basic formatting
                for row in employees:
                    print(f"RFID ID: {row['rfid_id']}, Name: {row['employee_name']}, Department: {row['department']}, Email: {row['email']}, Role: {row['role']}")
            else:
                print("No employees found.")
    except FileNotFoundError:
        print("Employee data file not found.")

def add_food_item():
    filename = 'food_items.csv'
    print("\n--- Add New Food Item ---")
    item_id = input("Enter Item ID: ").strip()
    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()
    price_input = input("Enter Price: ").strip()
    try:
        price = float(price_input)
    except ValueError:
        print("Price must be a number. Please try again.")
        return
    if not item_id or not item_name or not category:
        print("All fields are required. Please try again.")
        return
    # Check for duplicate Item IDs
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['item_id'] == item_id:
                print(f"Item ID {item_id} already exists. Please use a unique Item ID.")
                return
    # Append the new food item to the CSV file
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['item_id', 'item_name', 'category', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'item_id': item_id,
            'item_name': item_name,
            'category': category,
            'price': price
        })
    print(f"Food item '{item_name}' added successfully with Item ID {item_id}.")

def remove_food_item():
    filename = 'food_items.csv'
    print("\n--- Remove Food Item ---")
    item_id = input("Enter Item ID of the food item to remove: ").strip()
    food_items = []
    found = False
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['item_id'] != item_id:
                food_items.append(row)
            else:
                found = True
    if not found:
        print(f"No food item found with Item ID {item_id}.")
        return
    # Write updated list back to CSV
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['item_id', 'item_name', 'category', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(food_items)
    print(f"Food item with Item ID {item_id} removed successfully.")

def modify_food_item():
    filename = 'food_items.csv'
    print("\n--- Modify Food Item ---")
    item_id = input("Enter Item ID of the food item to modify: ").strip()
    food_items = []
    found = False
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['item_id'] == item_id:
                found = True
                print(f"Current Data: {row}")
                item_name = input("Enter new Item Name (leave blank to keep current): ").strip() or row['item_name']
                category = input("Enter new Category (leave blank to keep current): ").strip() or row['category']
                price_input = input("Enter new Price (leave blank to keep current): ").strip()
                price = row['price']
                if price_input:
                    try:
                        price = float(price_input)
                    except ValueError:
                        print("Invalid price entered. Keeping current price.")
                row.update({
                    'item_name': item_name,
                    'category': category,
                    'price': price
                })
            food_items.append(row)
    if not found:
        print(f"No food item found with Item ID {item_id}.")
        return
    # Write updated list back to CSV
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['item_id', 'item_name', 'category', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(food_items)
    print(f"Food item with Item ID {item_id} modified successfully.")

def list_all_food_items():
    filename = 'food_items.csv'
    print("\n--- List of All Food Items ---")
    try:
        with open(filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            food_items = [row for row in reader]
            if food_items:
                headers = ['item_id', 'item_name', 'category', 'price']
                # If using tabulate
                # print(tabulate(food_items, headers=headers, tablefmt='grid'))
                # If not using tabulate, use basic formatting
                for row in food_items:
                    print(f"Item ID: {row['item_id']}, Name: {row['item_name']}, Category: {row['category']}, Price: {row['price']}")
            else:
                print("No food items found.")
    except FileNotFoundError:
        print("Food items file not found.")

def main():
    while True:
        print("\n--- Cafeteria Checkout Simulation ---")
        rfid_id = receive_rfid_data()
        if rfid_id == '0000000000':
            print("Exiting program.")
            break
        employee_data = get_employee_data(rfid_id)
        if not employee_data:
            continue  # Skip if no employee is found
        if employee_data.get('role', 'user') == 'admin':
            admin_menu()
            continue

        # Present options to the user
        print("\nPlease select an option:")
        print("1. Make a Purchase")
        print("2. Settle Account")
        option = input("Enter your choice (1 or 2): ").strip()
        if option == '1':
            # Make a Purchase
            food_items = load_food_items()
            if not food_items:
                print("No food items available.")
                continue
            items = capture_items(food_items)
            if items is None:
                continue  # Restart if invalid items were entered

            # Calculate the total cost
            total_cost = sum(float(item['price']) for item in items)
            item_names = [item['item_name'] for item in items]

            # Generate a new transaction ID
            transaction_id = get_new_transaction_id()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            transaction = {
                'transaction_id': transaction_id,
                'timestamp': timestamp,
                'employee_id': employee_data['rfid_id'],
                'employee_name': employee_data['employee_name'],
                'transaction_type': 'Purchase',
                'items': ', '.join(item_names),
                'amount': f"{total_cost:.2f}"
            }

            log_transaction(transaction)
            print(f"Purchase Recorded: {transaction}")

        elif option == '2':
            # Settle Account
            outstanding_balance = calculate_outstanding_balance(employee_data['rfid_id'])
            print(f"Your outstanding balance is: ${outstanding_balance:.2f}")
            if outstanding_balance <= 0:
                print("You have no outstanding balance.")
                continue
            payment_input = input("Enter the amount you would like to pay: ").strip()
            try:
                payment_amount = float(payment_input)
                if payment_amount <= 0:
                    print("Payment amount must be positive.")
                    continue
                if payment_amount > outstanding_balance:
                    print(f"Payment amount cannot exceed the outstanding balance of ${outstanding_balance:.2f}.")
                    continue

                # Generate a new transaction ID
                transaction_id = get_new_transaction_id()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                transaction = {
                    'transaction_id': transaction_id,
                    'timestamp': timestamp,
                    'employee_id': employee_data['rfid_id'],
                    'employee_name': employee_data['employee_name'],
                    'transaction_type': 'Payment',
                    'items': '',
                    'amount': f"{payment_amount:.2f}"
                }

                log_transaction(transaction)
                print(f"Payment Recorded: {transaction}")
                new_balance = outstanding_balance - payment_amount
                print(f"Your new outstanding balance is: ${new_balance:.2f}")

            except ValueError:
                print("Invalid payment amount. Please enter a numeric value.")
                continue
        else:
            print("Invalid option selected. Please try again.")

if __name__ == '__main__':
    main()