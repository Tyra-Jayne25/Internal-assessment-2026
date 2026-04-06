import pygame
pygame.init()

# ===== CONSTANTS =====
WIDTH, HEIGHT = 1000, 650
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GREY = (220, 220, 220)

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

MAX_TABLES = 10
MAX_ITEM_QUANTITY = 5

# ===== ORIGINAL MENU ITEMS (REORGANISED INTO CATEGORIES) =====
MENU = {
    "Beverages": {
        "Cold Drinks": {
            "Iced Coffee": 3.00,
            "Iced Tea": 2.50,
            "Lemonade": 2.75,
            "Smoothie": 4.00,
            "Soda": 1.50
        },
        "Hot Drinks": {
            "Coffee": 2.50,
            "Tea": 2.00,
            "Hot Chocolate": 3.00,
            "Espresso": 2.75,
            "Latte": 3.50
        }
    },
    "Food": {
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
}

# ===== GLOBAL VARIABLES =====
available_tables = set(range(1, MAX_TABLES + 1))
current_order = {}
order_type = None
customer_name = None
table_number = None

# ===== PLACEHOLDER FUNCTIONS (KEEPING THESE EXACTLY AS YOU SAID) =====
def get_order_type(): pass
def get_dine_in_table(): pass
def get_customer_name(): pass
def display_order_summary(): pass
def confirm_order(): pass
def release_table(): pass
def process_order(): pass

def reset_order():
    global current_order, order_type, customer_name, table_number
    current_order = {}
    order_type = None
    customer_name = None
    table_number = None

# ===== GUI SETUP =====
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System")

# ===== DRAW BUTTON =====
def draw_button(text, x, y, w, h, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font_medium.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

# ===== SIDEBAR (LEFT CATEGORY LIST) =====
def draw_sidebar():
    pygame.draw.rect(screen, GREY, (0, 0, 200, HEIGHT))
    title = font_medium.render("CATEGORIES", True, BLACK)
    screen.blit(title, (20, 20))

    button_bev = draw_button("Beverages", 20, 80, 160, 60)
    button_food = draw_button("Food", 20, 160, 160, 60)

    return button_bev, button_food

# ===== SUBCATEGORY + ITEM SCREEN =====
def draw_subcategory_screen(category):
    screen.fill(WHITE)
    button_bev, button_food = draw_sidebar()

    subcats = list(MENU[category].keys())
    left_sub = subcats[0]
    right_sub = subcats[1]

    # Titles
    screen.blit(font_medium.render(left_sub, True, BLACK), (250, 40))
    screen.blit(font_medium.render(right_sub, True, BLACK), (600, 40))

    button_positions = {}

    # LEFT COLUMN
    y = 100
    for item, price in MENU[category][left_sub].items():
        screen.blit(font_small.render(f"{item} - £{price:.2f}", True, BLACK), (250, y))

        qty = current_order.get(item, 0)
        screen.blit(font_small.render(str(qty), True, BLACK), (480, y))

        minus = pygame.Rect(440, y, 30, 30)
        plus = pygame.Rect(520, y, 30, 30)

        pygame.draw.rect(screen, RED, minus)
        pygame.draw.rect(screen, GREEN, plus)
        screen.blit(font_small.render("-", True, WHITE), (448, y))
        screen.blit(font_small.render("+", True, WHITE), (528, y))

        button_positions[item] = (plus, minus)
        y += 50

    # RIGHT COLUMN
    y = 100
    for item, price in MENU[category][right_sub].items():
        screen.blit(font_small.render(f"{item} - £{price:.2f}", True, BLACK), (600, y))

        qty = current_order.get(item, 0)
        screen.blit(font_small.render(str(qty), True, BLACK), (830, y))

        minus = pygame.Rect(790, y, 30, 30)
        plus = pygame.Rect(870, y, 30, 30)

        pygame.draw.rect(screen, RED, minus)
        pygame.draw.rect(screen, GREEN, plus)
        screen.blit(font_small.render("-", True, WHITE), (798, y))
        screen.blit(font_small.render("+", True, WHITE), (878, y))

        button_positions[item] = (plus, minus)
        y += 50

    button_back = draw_button("Back", 250, 550, 150, 50)

    return button_bev, button_food, button_back, button_positions

# ===== MAIN LOOP =====
running = True
current_screen = "main_menu"
current_category = None

while running:
    screen.fill(WHITE)

    # MAIN MENU
    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (250, 150))

        button_start = draw_button("Start New Order", 350, 300, 300, 70)
        button_release = draw_button("Release Table", 350, 380, 300, 70)
        button_quit = draw_button("Quit", 350, 460, 300, 70)

    # CATEGORY SELECT SCREEN
    elif current_screen == "category_select":
        button_bev, button_food = draw_sidebar()

    # SUBCATEGORY SCREEN
    elif current_screen == "subcategory":
        button_bev, button_food, button_back, button_positions = draw_subcategory_screen(current_category)

    # ===== EVENT HANDLING =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "main_menu":
                if button_start.collidepoint(event.pos):
                    current_screen = "category_select"

                if button_release.collidepoint(event.pos):
                    print("Release Table clicked (GUI coming in later versions)")

                if button_quit.collidepoint(event.pos):
                    running = False

            elif current_screen == "category_select":
                if button_bev.collidepoint(event.pos):
                    current_category = "Beverages"
                    current_screen = "subcategory"
                if button_food.collidepoint(event.pos):
                    current_category = "Food"
                    current_screen = "subcategory"

            elif current_screen == "subcategory":
                if button_back.collidepoint(event.pos):
                    current_screen = "category_select"

                # Handle + and - buttons
                for item, (plus, minus) in button_positions.items():
                    if plus.collidepoint(event.pos):
                        current_order[item] = min(current_order.get(item, 0) + 1, MAX_ITEM_QUANTITY)
                    if minus.collidepoint(event.pos):
                        current_order[item] = max(current_order.get(item, 0) - 1, 0)

    pygame.display.update()

pygame.quit()