# Cafe Ordering System - Basic Functionality

# ===== CONSTANTS =====
MENU_ITEMS = {
    "Hot Drinks": {
        "Coffee": 2.50, 
        "Tea": 2.00, 
        "Hot Chocolate": 3.00, 
        "Espresso": 2.75, 
        "Latte": 3.50
    },
    "Cold Drinks:": {
        "Iced Coffee": 3.00,
        "Iced Tea": 2.50,
        "Lemonade": 2.75,
        "Smoothie": 4.00,
        "Soda": 1.50
    }, 
    "Snacks": {
        "Croissant": 2.00,
        "Muffin": 2.50,
        "Scone": 2.25,
        "Sandwich": 3.00,
        "Cookie": 1.75
    }, 
    "Meals": {
        "Salad": 5.00,
        "Hot Chips": 4.50,
        "Quiche": 6.00,
        "Pasta": 7.50,
        "Burger": 8.00
    }
}

MAX_TABLES = 10
MAX_ITEM_QUANTITY = 5 

# ===== GLOBAL VARIABLES =====
available_tables = set(range(1, MAX_TABLES + 1 ))
current_order = {}
order_type = None # dine-in or takeaway
customer_name = None
table_number = None

# ===== FUNCTIONS =====
def display_menu(): #display menu items and prices
    print("====================================")
    print("WELCOME TO OUR CAFE")
    print("====================================")
    
    for category, items in MENU_ITEMS.items():
        print("")
        print(category + ":")
        print("------------------------------------")
        for item, price in items.items():
            print("  " + item + " - £" + str(price))

# Order type selection
def get_order_type(): 
    global order_type

    while True:
        print("")
        print("====================================")
        print("ORDER TYPE")
        print("====================================")
        print("1. Dine-in")
        print("2. Takeaway")
        choice = input("Select order type (1 or 2): ").strip()

        if choice == "1":
            order_type = "Dine-in"
            break
        elif choice == "2":
            order_type = "Takeaway"
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

def get_dine_in_table(): #assign table number to customer if they choose dine-in and check for table availability, if no tables are available, inform the customer and ask them to wait for the next available table.
    global table_number, available_tables
    
    if not available_tables:
        print("Sorry, no tables avaliable. Please wait for the next avaliable table.")
        return False
    
    table_number = min(available_tables)
    available_tables.remove(table_number)
    print(f"\nYour table number: {table_number}") 
    return True

def get_customer_name(): #prompt customer to enter their name for their takeaway order
    global customer_name

    while True:
        name = input("\nPlease enter your name: ").strip()
        if name:
            customer_name = name
            break
        else:
            print("Name cannot be empty. Please try again.")

def take_order(): # allow customer to select items and quantities for their order
    global current_order
    current_order = {}

    print("=====================================")
    print("ADD ITEMS TO YOUR ORDER")
    print("=====================================")

    for category, items in MENU_ITEMS.items():
        print(f"\n{category}:")
        for item, price in items.items():
            while True:
                quantity_input = input(f" {item} - £{price:.2f}) - Quantity (0 to skip): ").strip()
                try:
                    quantity = int(quantity_input)
                except ValueError:
                    print("Invalid input. Please enter a whole number.")
                    continue

                if quantity < 0 or quantity > MAX_ITEM_QUANITITY:
                    print(f"Please enter a number between 0 and {MAX_ITEM_QUANTITY}.")
                    continue
                if quantity > 0:
                    current_order[item] = {"quantity": quantity, "price": price}
                break

def display_order_summary(): #display itemised order summary with total cost
    if not current_order:
        print("\nYour order is empty")
        return 0
    
    print("=====================================")
    print("ORDER SUMMARY")
    print("=====================================")
    
    total_cost = 0
    
    for item, details in current_order.items():
        quantity = details["quantity"]
        price = details["price"]
        item_total = quantity * price
        total_cost += item_total
        print(f"{item} x {quantity} - £{item_total:.2f}")

    print("=====================================")
    print(f"{'TOTAL':<25} {'':5} £{total_cost:.2f}")
    print("=====================================")
    return total_cost

def confirm_order(): #ask customer to confirm or cancel their order
    while True:
        choice = input("\nComplete order? (yes/no): ").strip().lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def release_table(): # alow staff to release a table back to aaliable
    global available_tables
    
    print("=====================================")
    print("RELEASE TABLE")
    print("====================================")
    
    occupied = sorted(set(range(1, MAX_TABLES + 1)) - available_tables)
    if not occupied:
        print("No tables are currently occupied.")
        return
    
    print(f"Currently occupied tables: {occupied}")
    
    while True:
        table_input = input("Enter table number to release (0 to cancel): ").strip()
        try:
            table = int(table_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        
        if table == 0:
            break
        if 1 <= table <= MAX_TABLES and table not in available_tables:
            available_tables.add(table)
            print(f"Table {table} has been released.")
            break
        else:
            print(f"Invalid table number. Please enter a number between 1 and {MAX_TABLES}.")

def process_order(): #complete the order and print final details
    total = display_order_summary()
    
    print(f"\nOrder Type: {order_type.upper()}")
    
    if order_type == "dine-in":
        print(f"Table Number: {table_number}")
    else:
        print(f"Customer Name: {customer_name}")
    
    print("\nOrder completed! Thank you for your purchase.")
    return total


def reset_order():
    """Reset all order variables for next customer."""
    global current_order, order_type, customer_name, table_number
    current_order = {}
    order_type = None
    customer_name = None
    table_number = None

#Main program loop
def start_system():
    print("=====================================")
    print("Welcome to the Cafe Ordering System!")
    print("=====================================")  

    while True:
        print("\nMAIN MENU:")
        print("1. Start New Order")
        print("2. Release Table")
        print("3. Quit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print("\nPress Enter to start your order (or 'q' to cancel)...")
            user_input = input().strip().lower()
            if user_input == "q":
                continue

            display_menu()
            get_order_type()

            if order_type == "Dine-in":
                if not get_dine_in_table():
                    reset_order()
                    continue

            else:
                get_customer_name()
            take_order()

            if current_order and confirm_order():
                process_order()
            else:
                print("Order cancelled.")
            reset_order()

        elif choice == "2":
            release_table()

        elif choice == "3":
            print("Thank you for using our system. Goodbye!")
            break

        else:
            print("Invalid option. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    start_system()