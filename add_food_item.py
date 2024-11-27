import csv
import os

def add_food_item():
    # Define the CSV file name
    filename = 'food_items.csv'
    
    # Check if the CSV file exists; if not, create it with headers
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['item_id', 'item_name', 'category', 'price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
    # Collect food item information
    print("\n--- Add New Food Item ---")
    item_id = input("Enter Item ID: ").strip()
    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()
    price_input = input("Enter Price: ").strip()
    
    # Validate inputs
    if not item_id or not item_name or not category or not price_input:
        print("All fields are required. Please try again.")
        return
    
    # Validate price
    try:
        price = float(price_input)
    except ValueError:
        print("Price must be a number. Please try again.")
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

if __name__ == '__main__':
    add_food_item()