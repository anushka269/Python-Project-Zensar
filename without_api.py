import mysql.connector

# Database Connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="CafeDB"
    )

# Add Menu Item
def add_menu_item():
    name = input("Enter item name: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO MenuItems (ItemName, Category, Price) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, category, price))
    db.commit()
    print("Menu item added successfully!")
    cursor.close()
    db.close()

# View Menu Items
def view_menu():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM MenuItems")
    for item in cursor.fetchall():
        print(item)
    cursor.close()
    db.close()

# Place an Order
def place_order():
    item_id = int(input("Enter item ID: "))
    quantity = int(input("Enter quantity: "))
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Orders (ItemID, Quantity, OrderDate) VALUES (%s, %s, CURDATE())"
    cursor.execute(query, (item_id, quantity))
    db.commit()
    print("Order placed successfully!")
    cursor.close()
    db.close()

# View Inventory
def view_inventory():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Inventory")
    for item in cursor.fetchall():
        print(item)
    cursor.close()
    db.close()

# Main Menu
def main():
    while True:
        print("\n--- Café Management System ---")
        print("1. Add Menu Item")
        print("2. View Menu")
        print("3. Place Order")
        print("4. View Inventory")
        print("5. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            add_menu_item()
        elif choice == '2':
            view_menu()
        elif choice == '3':
            place_order()
        elif choice == '4':
            view_inventory()
        elif choice == '5':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
