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
GREEN = (0, 180, 0)
RED = (200, 0, 0)

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# ===== GLOBAL VARIABLES =====
available_tables = set(range(1, MAX_TABLES + 1 ))
current_order = {}
order_type = None # dine-in or takeaway
customer_name = None
table_number = None

# ===== FUNCTIONS =====
# ===== FUNCTIONS (KEPT FOR DEVELOPMENT EVIDENCE) =====
def display_menu():
    screen.fill(WHITE)

    welcome = font_large.render("WELCOME TO OUR CAFE", True, BLACK)
    screen.blit(welcome, (180, 20))

    y_offset = 120
    button_positions = {}  # store + and - button rects

    for category, items in MENU_ITEMS.items():
        cat_text = font_medium.render(category, True, BLACK)
        screen.blit(cat_text, (50, y_offset))
        y_offset += 40

        for item, price in items.items():
            item_text = font_small.render(f"{item} - £{price:.2f}", True, BLACK)
            screen.blit(item_text, (80, y_offset))

            qty = current_order.get(item, 0)
            qty_text = font_small.render(str(qty), True, BLACK)
            screen.blit(qty_text, (500, y_offset))

            plus_rect = pygame.Rect(550, y_offset, 30, 30)
            pygame.draw.rect(screen, GREEN, plus_rect)
            screen.blit(font_small.render("+", True, WHITE), (558, y_offset))

            minus_rect = pygame.Rect(600, y_offset, 30, 30)
            pygame.draw.rect(screen, RED, minus_rect)
            screen.blit(font_small.render("-", True, WHITE), (610, y_offset))

            button_positions[item] = (plus_rect, minus_rect)

            y_offset += 40

        y_offset += 20

    back_button = draw_button("Back", 50, 500, 150, 50)
    return button_positions, back_button

def get_order_type():
    pass

def get_dine_in_table():
    pass

def get_customer_name():
    pass

def take_order(item, increase=True):
    if increase:
        current_order[item] = min(current_order.get(item, 0) + 1, MAX_ITEM_QUANTITY)
    else:
        current_order[item] = max(current_order.get(item, 0) - 1, 0)

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

# GUI MAIN LOOP
running = True
while running:
    screen.fill(WHITE)

    # MAIN MENU SCREEN
    running = True
button_positions = {}

while running:
    screen.fill(WHITE)

    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (200, 50))

        btn_start = draw_button("Start New Order", 300, 200, 250, 60)
        btn_release = draw_button("Release Table", 300, 300, 250, 60)
        btn_quit = draw_button("Quit", 300, 400, 250, 60)

    if current_screen == "menu":
        button_positions, btn_back = display_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "main_menu":
                if btn_start.collidepoint(event.pos):
                    current_screen = "menu"
                if btn_release.collidepoint(event.pos):
                    print("Release Table clicked (GUI not added yet)")
                if btn_quit.collidepoint(event.pos):
                    running = False

            if current_screen == "menu":
                if btn_back.collidepoint(event.pos):
                    current_screen = "main_menu"

                for item, (plus_rect, minus_rect) in button_positions.items():

                    if plus_rect.collidepoint(event.pos):
                        take_order(item, increase=True)

                    if minus_rect.collidepoint(event.pos):
                        take_order(item, increase=False)

    pygame.display.update()

pygame.quit()