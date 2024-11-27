import csv
from datetime import datetime
import os

def receive_rfid_data():
    rfid_id = input("Enter RFID ID (simulated scan): ").strip()
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
            print(f"Employee Data Found: {employee_data}")
        else:
            print(f"No employee found for RFID ID: {rfid_id}")
    except FileNotFoundError:
        print("Employee data file not found.")
    return employee_data

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

def log_transaction(employee_data, items):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item_names = [item['item_name'] for item in items]
    transaction = {
        'employee_id': employee_data.get('rfid_id', 'Unknown'),
        'employee_name': employee_data.get('employee_name', 'Unknown'),
        'items': item_names,
        'timestamp': timestamp
    }
    print(f"Transaction Logged: {transaction}")
    # Append to a log file
    with open('transactions.log', 'a') as f:
        f.write(f"{transaction}\n")

def main():
    while True:
        print("\n--- Cafeteria Checkout Simulation ---")
        rfid_id = receive_rfid_data()
        employee_data = get_employee_data(rfid_id)
        if not employee_data:
            continue  # Skip if no employee is found
        food_items = load_food_items()
        if not food_items:
            print("No food items available.")
            continue
        items = capture_items(food_items)
        if items is None:
            continue  # Restart if invalid items were entered
        log_transaction(employee_data, items)
        # Option to exit the loop
        cont = input("Process another transaction? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == '__main__':
    main()