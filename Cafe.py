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
MAX_ITEM_QUANITITY = 5 

# ===== GLOBAL VARIABLES =====
available_tables = list(range(1, MAX_TABLES + 1 ))
current_order = {}
order_type = None # dine-in or takeaway
customer_name = None
table_number = None

# ===== FUNCTIONS =====
def display_menu():
    print("")
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

def get_dine_in_table(): 
    """Assign a table for dine-in customers"""
    global table_number, available_tables
    
    if not available_tables:
        print("Sorry, no tables avaliable. Please wait for the next avaliable table.")
        return False
    
    table_number = min(available_tables)
    available_tables.remove(table_number)
    print(f"\nYour table number: {table_number}") 
    return True

def get_customer_name():
    global customer_name

    while True:
        name = input("\nPlease enter your name: ").strip()
        if name:
            customer_name = name
            break
        else:
            print("Name cannot be empty. Please try again.")



