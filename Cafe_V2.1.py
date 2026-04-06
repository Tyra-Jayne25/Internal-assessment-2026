import pygame
pygame.init()
# Cafe Ordering System - Basic GUI input and output, with improved user experience and error handling

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

# ===== GUI CONSTANTS =====
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)

# ===== GLOBAL VARIABLES =====
available_tables = set(range(1, MAX_TABLES + 1 ))
current_order = {}
order_type = None # dine-in or takeaway
customer_name = None
table_number = None

# ===== FUNCTIONS =====
# ===== FUNCTIONS (KEPT FOR DEVELOPMENT EVIDENCE) =====
def display_menu():
    pass

def get_order_type():
    pass

def get_dine_in_table():
    pass

def get_customer_name():
    pass

def take_order():
    pass

def display_order_summary():
    pass

def confirm_order():
    pass

def release_table():
    pass

def process_order():
    pass

def reset_order():
    global current_order, order_type, customer_name, table_number
    current_order = {}
    order_type = None
    customer_name = None
    table_number = None

# Basic GUI setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System - GUI Version")

current_screen = "main_menu"

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BLUE, (x, y, w, h))
    label = font_medium.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

running = True
while running:
    screen.fill(WHITE)

    # MAIN MENU SCREEN
    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (200, 50))

        btn_start = draw_button("Start New Order", 300, 200, 250, 60)
        btn_release = draw_button("Release Table", 300, 300, 250, 60)
        btn_quit = draw_button("Quit", 300, 400, 250, 60)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main_menu":
                if btn_start.collidepoint(event.pos):
                    print("Start New Order clicked (GUI not added yet)")
                if btn_release.collidepoint(event.pos):
                    print("Release Table clicked (GUI not added yet)")
                if btn_quit.collidepoint(event.pos):
                    running = False

    pygame.display.update()

pygame.quit()