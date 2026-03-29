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