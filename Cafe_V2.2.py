import pygame
pygame.init()

# ===== CONSTANTS =====
WIDTH, HEIGHT = 1000, 650
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
BLUE_DARK = (40, 90, 140)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GREY = (220, 220, 220)
LIGHT_GREY = (240, 240, 240)

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

MAX_ITEM_QUANTITY = 5

# ===== MENU =====
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
current_order = {}
current_screen = "main_menu"
current_category = "Beverages"

# ===== PLACEHOLDER FUNCTIONS =====
def get_order_type(): pass
def get_dine_in_table(): pass
def get_customer_name(): pass
def display_order_summary(): pass
def confirm_order(): pass
def release_table(): pass
def process_order(): pass

def reset_order():
    global current_order
    current_order = {}

# ===== GUI SETUP =====
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System - Version 2.3")

# ===== DRAW BUTTON =====
def draw_button(text, x, y, w, h, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    label = font_medium.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + 10))
    return pygame.Rect(x, y, w, h)

# ===== SIDEBAR =====
def draw_sidebar(selected):
    pygame.draw.rect(screen, GREY, (0, 0, 200, HEIGHT))

    bev_color = BLUE_DARK if selected == "Beverages" else BLUE
    food_color = BLUE_DARK if selected == "Food" else BLUE

    button_bev = draw_button("Beverages", 20, 80, 160, 60, bev_color)
    button_food = draw_button("Food", 20, 160, 160, 60, food_color)

    return button_bev, button_food

# ===== ORDERING SCREEN =====
def draw_ordering_screen(category):
    screen.fill(WHITE)

    # Top bar
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    screen.blit(font_medium.render("Cafe Name", True, WHITE), (20, 10))

    # Sidebar
    button_bev, button_food = draw_sidebar(category)

    # Subcategories
    subcats = list(MENU[category].keys())
    left_sub = subcats[0]
    right_sub = subcats[1]

    screen.blit(font_medium.render(left_sub, True, BLACK), (250, 80))
    screen.blit(font_medium.render(right_sub, True, BLACK), (600, 80))

    button_positions = {}

    # LEFT COLUMN
    y = 140
    for item, price in MENU[category][left_sub].items():
        screen.blit(font_small.render(f"{item}", True, BLACK), (250, y))
        screen.blit(font_small.render(f"£{price:.2f}", True, BLACK), (400, y))

        qty = current_order.get(item, 0)
        screen.blit(font_small.render(str(qty), True, BLACK), (520, y))

        minus = pygame.Rect(480, y, 30, 30)
        plus = pygame.Rect(560, y, 30, 30)

        pygame.draw.rect(screen, RED, minus)
        pygame.draw.rect(screen, GREEN, plus)
        screen.blit(font_small.render("-", True, WHITE), (488, y))
        screen.blit(font_small.render("+", True, WHITE), (568, y))

        button_positions[item] = (plus, minus)
        y += 50

    # RIGHT COLUMN
    y = 140
    for item, price in MENU[category][right_sub].items():
        screen.blit(font_small.render(f"{item}", True, BLACK), (600, y))
        screen.blit(font_small.render(f"£{price:.2f}", True, BLACK), (750, y))

        qty = current_order.get(item, 0)
        screen.blit(font_small.render(str(qty), True, BLACK), (870, y))

        minus = pygame.Rect(830, y, 30, 30)
        plus = pygame.Rect(910, y, 30, 30)

        pygame.draw.rect(screen, RED, minus)
        pygame.draw.rect(screen, GREEN, plus)
        screen.blit(font_small.render("-", True, WHITE), (838, y))
        screen.blit(font_small.render("+", True, WHITE), (918, y))

        button_positions[item] = (plus, minus)
        y += 50

    # Bottom bar
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 80, WIDTH, 80))

    total_cost = sum(
        MENU[cat][sub][item] * qty
        for cat in MENU
        for sub in MENU[cat]
        for item, qty in current_order.items()
        if item in MENU[cat][sub]
    )

    screen.blit(font_medium.render(f"Cost: £{total_cost:.2f}", True, WHITE), (20, HEIGHT - 60))

    see_order_btn = draw_button("See Order", 300, HEIGHT - 70, 150, 50)
    cancel_btn = draw_button("Cancel Order", 500, HEIGHT - 70, 150, 50)
    complete_btn = draw_button("Complete Order", 700, HEIGHT - 70, 180, 50)

    return button_bev, button_food, see_order_btn, cancel_btn, complete_btn, button_positions

# ===== ORDER SUMMARY SCREEN =====
def draw_order_summary():
    screen.fill(WHITE)

    # Top bar
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    screen.blit(font_medium.render("ORDER", True, WHITE), (20, 10))

    # White box for order list
    box = pygame.Rect(80, 100, 840, 450)
    pygame.draw.rect(screen, LIGHT_GREY, box, border_radius=12)

    # Filter out items with qty 0
    filtered_items = [(item, qty) for item, qty in current_order.items() if qty > 0]

    # Two-column layout
    col1_x = 120
    col2_x = 520
    y = 140
    count = 0

    for item, qty in filtered_items:
        price = None
        for cat in MENU:
            for sub in MENU[cat]:
                if item in MENU[cat][sub]:
                    price = MENU[cat][sub][item]

        x = col1_x if count % 2 == 0 else col2_x

        screen.blit(font_small.render(f"{item} x{qty} - £{price * qty:.2f}", True, BLACK), (x, y))

        if count % 2 == 1:
            y += 40

        count += 1

    # Total cost
    total_cost = sum(
        MENU[cat][sub][item] * qty
        for cat in MENU
        for sub in MENU[cat]
        for item, qty in current_order.items()
        if item in MENU[cat][sub]
    )

    screen.blit(font_medium.render(f"Total: £{total_cost:.2f}", True, BLACK), (120, 500))

    back_btn = draw_button("Back", 120, 540, 150, 50)
    return back_btn

# ===== MAIN LOOP =====
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # MAIN MENU
            if current_screen == "main_menu":
                button_start = draw_button("Start New Order", 350, 300, 300, 70)
                button_release = draw_button("Release Table", 350, 380, 300, 70)
                button_quit = draw_button("Quit", 350, 460, 300, 70)

                if button_start.collidepoint(event.pos):
                    current_screen = "ordering"

                if button_quit.collidepoint(event.pos):
                    running = False

            # ORDERING SCREEN
            elif current_screen == "ordering":
                button_bev, button_food, see_order_btn, cancel_btn, complete_btn, button_positions = draw_ordering_screen(current_category)

                if button_bev.collidepoint(event.pos):
                    current_category = "Beverages"

                if button_food.collidepoint(event.pos):
                    current_category = "Food"

                if see_order_btn.collidepoint(event.pos):
                    current_screen = "order_summary"

                if cancel_btn.collidepoint(event.pos):
                    reset_order()
                    current_screen = "main_menu"

                # Handle + and -
                for item, (plus, minus) in button_positions.items():
                    if plus.collidepoint(event.pos):
                        current_order[item] = min(current_order.get(item, 0) + 1, MAX_ITEM_QUANTITY)
                    if minus.collidepoint(event.pos):
                        current_order[item] = max(current_order.get(item, 0) - 1, 0)

            # ORDER SUMMARY
            elif current_screen == "order_summary":
                back_btn = draw_order_summary()
                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

    # Draw screens
    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (250, 150))
        draw_button("Start New Order", 350, 300, 300, 70)
        draw_button("Release Table", 350, 380, 300, 70)
        draw_button("Quit", 350, 460, 300, 70)

    elif current_screen == "ordering":
        draw_ordering_screen(current_category)

    elif current_screen == "order_summary":
        draw_order_summary()

    pygame.display.update()

pygame.quit()