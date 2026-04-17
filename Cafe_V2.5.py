import pygame
import os
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
DARK_GREY = (160, 160, 160)

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
current_category = None
current_subcategory = None

popup_item = None
popup_qty = 1

# ===== GUI SETUP =====
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System - Version 2.4")

# ===== IMAGE LOADING (Taniwha-style) =====
def load_image(filename, fallback_color, size):
    if os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            img = pygame.transform.scale(img, size)
            return img
        except:
            pass

    surf = pygame.Surface(size)
    surf.fill(fallback_color)
    return surf

# ===== LOAD ALL ITEM IMAGES =====
iced_coffee_img = load_image("Iced Coffee.png", GREY, (60, 60))
iced_tea_img = load_image("Iced Tea.png", GREY, (60, 60))
lemonade_img = load_image("Lemonade.png", GREY, (60, 60))
smoothie_img = load_image("Smoothie.png", GREY, (60, 60))
soda_img = load_image("Soda.png", GREY, (60, 60))

coffee_img = load_image("Coffee.png", GREY, (60, 60))
tea_img = load_image("Tea.png", GREY, (60, 60))
hot_chocolate_img = load_image("Hot Chocolate.png", GREY, (60, 60))
espresso_img = load_image("Espresso.png", GREY, (60, 60))
latte_img = load_image("Latte.png", GREY, (60, 60))

croissant_img = load_image("Croissant.png", GREY, (60, 60))
muffin_img = load_image("Muffin.png", GREY, (60, 60))
scone_img = load_image("Scone.png", GREY, (60, 60))
sandwich_img = load_image("Sandwich.png", GREY, (60, 60))
cookie_img = load_image("Cookie.png", GREY, (60, 60))

salad_img = load_image("Salad.png", GREY, (60, 60))
hot_chips_img = load_image("Hot Chips.png", GREY, (60, 60))
quiche_img = load_image("Quiche.png", GREY, (60, 60))
pasta_img = load_image("Pasta.png", GREY, (60, 60))
burger_img = load_image("Burger.png", GREY, (60, 60))

# ===== MAP ITEM NAMES TO IMAGES =====
ITEM_IMAGES = {
    "Iced Coffee": iced_coffee_img,
    "Iced Tea": iced_tea_img,
    "Lemonade": lemonade_img,
    "Smoothie": smoothie_img,
    "Soda": soda_img,

    "Coffee": coffee_img,
    "Tea": tea_img,
    "Hot Chocolate": hot_chocolate_img,
    "Espresso": espresso_img,
    "Latte": latte_img,

    "Croissant": croissant_img,
    "Muffin": muffin_img,
    "Scone": scone_img,
    "Sandwich": sandwich_img,
    "Cookie": cookie_img,

    "Salad": salad_img,
    "Hot Chips": hot_chips_img,
    "Quiche": quiche_img,
    "Pasta": pasta_img,
    "Burger": burger_img
}

# ===== DRAW BUTTON =====
def draw_button(text, x, y, w, h, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font_medium.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2,
                        y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# ===== SIDEBAR =====
def draw_sidebar():
    pygame.draw.rect(screen, GREY, (0, 0, 200, HEIGHT))

    bev_btn = draw_button("Beverages", 20, 80, 160, 60,
                          BLUE_DARK if current_category == "Beverages" else BLUE)
    food_btn = draw_button("Food", 20, 160, 160, 60,
                           BLUE_DARK if current_category == "Food" else BLUE)

    sub_buttons = []
    if current_category:
        x = 230
        y = 80
        for sub in MENU[current_category]:
            rect = draw_button(sub, x, y, 180, 50, DARK_GREY)
            sub_buttons.append((sub, rect))
            x += 200

    return bev_btn, food_btn, sub_buttons

# ===== ITEM GRID (3 per row) =====
def draw_item_grid():
    if not current_subcategory:
        return []

    items = MENU[current_category][current_subcategory]
    item_boxes = []

    x = 230
    y = 160
    count = 0

    for item, price in items.items():
        box = pygame.Rect(x, y, 200, 140)
        pygame.draw.rect(screen, LIGHT_GREY, box)

        # IMAGE
        screen.blit(ITEM_IMAGES[item], (x + 10, y + 10))

        screen.blit(font_small.render(item, True, BLACK), (x + 80, y + 15))
        screen.blit(font_small.render(f"${price:.2f}", True, BLACK), (x + 80, y + 50))

        item_boxes.append((item, box))

        count += 1
        if count % 3 == 0:
            x = 230
            y += 160
        else:
            x += 220

    return item_boxes

# ===== POPUP WINDOW =====
def draw_popup():
    global popup_qty

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    popup = pygame.Rect(250, 120, 500, 400)
    pygame.draw.rect(screen, WHITE, popup)

    close_btn = pygame.Rect(690, 130, 40, 40)
    pygame.draw.rect(screen, RED, close_btn)
    screen.blit(font_medium.render("X", True, WHITE), (701, 138))

    name_label = font_medium.render(popup_item, True, BLACK)
    screen.blit(name_label, (250 + (500 - name_label.get_width()) // 2, 150))

    img_x = 250 + (500 - 200) // 2
    popup_img = load_image(f"{popup_item}.png", GREY, (200, 150))
    screen.blit(popup_img, (img_x, 200))

    price = MENU[current_category][current_subcategory][popup_item]
    price_label = font_small.render(f"Price: £{price:.2f}", True, BLACK)
    screen.blit(price_label, (250 + (500 - price_label.get_width()) // 2, 360))

    minus_btn = pygame.Rect(380, 390, 40, 40)
    plus_btn = pygame.Rect(580, 390, 40, 40)
    pygame.draw.rect(screen, RED, minus_btn)
    pygame.draw.rect(screen, GREEN, plus_btn)

    qty_label = font_medium.render(str(popup_qty), True, BLACK)
    screen.blit(qty_label, (250 + (500 - qty_label.get_width()) // 2, 395))

    screen.blit(font_medium.render("-", True, WHITE), (394, 394))
    screen.blit(font_medium.render("+", True, WHITE), (592, 394))

    add_btn = draw_button("Add to Order", 350, 450, 300, 50, BLUE_DARK)

    return close_btn, minus_btn, plus_btn, add_btn

# ===== ORDER SUMMARY =====
def draw_order_summary():
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    screen.blit(font_medium.render("ORDER", True, WHITE), (20, 10))

    items = [(item, qty) for item, qty in current_order.items() if qty > 0]

    col1_x = 80
    col2_x = 500
    y = 140
    count = 0

    for item, qty in items:
        price = None
        for cat in MENU:
            for sub in MENU[cat]:
                if item in MENU[cat][sub]:
                    price = MENU[cat][sub][item]

        x = col1_x if count % 2 == 0 else col2_x

        screen.blit(font_small.render(f"{item} x{qty} - ${price * qty:.2f}", True, BLACK), (x, y))

        if count % 2 == 1:
            y += 40

        count += 1

    total_cost = sum(
        MENU[cat][sub][item] * qty
        for cat in MENU
        for sub in MENU[cat]
        for item, qty in current_order.items()
        if item in MENU[cat][sub]
    )

    screen.blit(font_medium.render(f"Total: ${total_cost:.2f}", True, BLACK), (60, 570))

    return draw_button("Back", 800, 560, 150, 50)

# ===== MAIN LOOP =====
running = True
item_boxes = []

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "main_menu":
                start_btn = draw_button("Start New Order", 350, 300, 300, 70)
                release_btn = draw_button("Release Table", 350, 380, 300, 70)
                quit_btn = draw_button("Quit", 350, 460, 300, 70)

                if start_btn.collidepoint(event.pos):
                    current_screen = "ordering"

                if quit_btn.collidepoint(event.pos):
                    running = False

            elif current_screen == "ordering":

                bev_btn, food_btn, sub_btns = draw_sidebar()

                if bev_btn.collidepoint(event.pos):
                    current_category = "Beverages"
                    current_subcategory = None

                if food_btn.collidepoint(event.pos):
                    current_category = "Food"
                    current_subcategory = None

                for sub, rect in sub_btns:
                    if rect.collidepoint(event.pos):
                        current_subcategory = sub

                # POPUP ACTIVE — ONLY POPUP BUTTONS WORK
                if popup_item is not None:

                    close_btn, minus_btn, plus_btn, add_btn = draw_popup()

                    if close_btn.collidepoint(event.pos):
                        popup_item = None
                        continue

                    if minus_btn.collidepoint(event.pos):
                        popup_qty = max(1, popup_qty - 1)
                        continue

                    if plus_btn.collidepoint(event.pos):
                        popup_qty = min(MAX_ITEM_QUANTITY, popup_qty + 1)
                        continue

                    if add_btn.collidepoint(event.pos):
                        current_order[popup_item] = min(
                            MAX_ITEM_QUANTITY,
                            current_order.get(popup_item, 0) + popup_qty
                        )
                        popup_item = None
                        continue

                    continue

                # ONLY CHECK ITEM CLICKS IF POPUP IS CLOSED
                if popup_item is None and current_subcategory:
                    for item, rect in item_boxes:
                        if rect.collidepoint(event.pos):
                            popup_item = item
                            popup_qty = 1
                            break

                see_btn = draw_button("See Order", 260, HEIGHT - 72, 200, 55, BLUE_DARK)
                cancel_btn = draw_button("Cancel Order", 480, HEIGHT - 72, 200, 55, BLUE_DARK)
                complete_btn = draw_button("Complete Order", 700, HEIGHT - 72, 230, 55, BLUE_DARK)

                if see_btn.collidepoint(event.pos):
                    current_screen = "order_summary"

                if cancel_btn.collidepoint(event.pos):
                    current_order = {}
                    current_category = None
                    current_subcategory = None
                    current_screen = "main_menu"

                if complete_btn.collidepoint(event.pos):
                    pass  # placeholder

            elif current_screen == "order_summary":
                back_btn = draw_order_summary()
                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (250, 150))
        draw_button("Start New Order", 350, 300, 300, 70)
        draw_button("Release Table", 350, 380, 300, 70)
        draw_button("Quit", 350, 460, 300, 70)

    elif current_screen == "ordering":
        bev_btn, food_btn, sub_btns = draw_sidebar()
        item_boxes = draw_item_grid()

        total_cost = sum(
            MENU[cat][sub][item] * qty
            for cat in MENU
            for sub in MENU[cat]
            for item, qty in current_order.items()
            if item in MENU[cat][sub]
        )
        screen.blit(font_medium.render(f"Cost: ${total_cost:.2f}", True, BLACK), (20, HEIGHT - 60))

        draw_button("See Order", 260, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Cancel Order", 480, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Complete Order", 700, HEIGHT - 72, 230, 55, BLUE_DARK)

        if popup_item:
            draw_popup()

    elif current_screen == "order_summary":
        draw_order_summary()

    pygame.display.update()

pygame.quit()