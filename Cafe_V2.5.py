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

# ===== NEW GLOBALS FOR VERSION 2.5 =====
customer_name = ""
tables_available = [1,2,3,4,5,6,7,8,9,10]
assigned_table = None

# text input active flag for takeaway
input_active = False

# ===== GUI SETUP =====
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System - Version 2.5")

# ===== IMAGE LOADING =====
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

# ===== NEW PLACEHOLDER IMAGES =====
takeaway_img = load_image("Takeaway.png", GREY, (150, 150))
dinein_img = load_image("Dine-In.png", GREY, (150, 150))

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
    price_label = font_small.render(f"Price: ${price:.2f}", True, BLACK)
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

# ===== THANK YOU SCREEN =====
def draw_thank_you():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    title = font_large.render("Cafe Name", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    msg = font_medium.render("Thank You for Ordering at our Cafe!", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 20))

# ===== UPDATED ORDER TYPE SCREEN =====
def draw_order_type():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    title = font_medium.render("ORDER TYPE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    take_rect = pygame.Rect(200, 200, 250, 250)
    pygame.draw.rect(screen, LIGHT_GREY, take_rect)
    screen.blit(takeaway_img, (take_rect.x + 50, take_rect.y + 20))

    take_label = font_medium.render("Takeaway", True, BLACK)
    screen.blit(take_label, (take_rect.centerx - take_label.get_width()//2,
                             take_rect.y + 190))

    dine_rect = pygame.Rect(550, 200, 250, 250)
    pygame.draw.rect(screen, LIGHT_GREY, dine_rect)
    screen.blit(dinein_img, (dine_rect.x + 50, dine_rect.y + 20))

    dine_label = font_medium.render("Dine-In", True, BLACK)
    screen.blit(dine_label, (dine_rect.centerx - dine_label.get_width()//2,
                             dine_rect.y + 190))

    back_btn = draw_button("Back", WIDTH//2 - 150, 500, 300, 60)

    return dine_rect, take_rect, back_btn

# ===== UPDATED TAKEAWAY SCREEN =====
def draw_takeaway_name():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    title = font_medium.render("TAKEAWAY", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    prompt = font_medium.render("Enter your name:", True, BLACK)
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 200))

    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH//2 - 200, 260, 400, 60))
    name_text = font_medium.render(customer_name, True, BLACK)
    screen.blit(name_text, (WIDTH//2 - 190, 270))

    enter_btn = draw_button("Enter", WIDTH//2 - 150, 350, 300, 70)
    back_btn = draw_button("Back", WIDTH//2 - 150, 450, 300, 70)

    return enter_btn, back_btn

# ===== UPDATED DINE-IN SCREEN =====
def draw_dine_in():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    title = font_medium.render("DINE-IN", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    if len(tables_available) == 0:
        return None, None

    table_num = tables_available[0]

    label = font_medium.render("Your table number is:", True, BLACK)
    screen.blit(label, (WIDTH//2 - label.get_width()//2, 200))

    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH//2 - 75, 260, 150, 100))
    num = font_large.render(str(table_num), True, BLACK)
    screen.blit(num, (WIDTH//2 - num.get_width()//2, 280))

    enter_btn = draw_button("Enter", WIDTH//2 - 150, 450, 300, 70)
    return enter_btn, table_num

# ===== UPDATED REVIEW ORDER SCREEN =====
def draw_complete_order():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    title = font_medium.render("REVIEW ORDER", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

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
    total_label = font_medium.render(f"Total: ${total_cost:.2f}", True, BLACK)
    screen.blit(total_label, (60, 570))

    continue_btn = draw_button("Continue", WIDTH//2 - 100, 560, 200, 50)
    back_btn = draw_button("Back", WIDTH - 200, 560, 150, 50)

    return continue_btn, back_btn

# ===== NO TABLES SCREEN =====
def draw_no_tables():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = font_medium.render("NO TABLES AVAILABLE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    msg = font_medium.render("Sorry, no tables available. Please wait for the next available table.", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))

    back_btn = draw_button("Back", WIDTH//2 - 150, 450, 300, 70)
    return back_btn

# ===== RELEASE TABLE SCREEN (OPTION A GRID) =====
def draw_release_table():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = font_medium.render("RELEASE TABLE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    tables_rects = []
    all_tables = list(range(1, 11))
    used_tables = [t for t in all_tables if t not in tables_available]

    start_x = 200
    start_y = 140
    w, h = 100, 80
    gap_x = 40
    gap_y = 40

    for i, t in enumerate(all_tables):
        row = i // 5
        col = i % 5
        x = start_x + col * (w + gap_x)
        y = start_y + row * (h + gap_y)

        if t in used_tables:
            color = RED
        else:
            color = GREY

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, rect)

        label = font_medium.render(str(t), True, WHITE if t in used_tables else BLACK)
        screen.blit(label, (rect.centerx - label.get_width()//1,
                            rect.centery - label.get_height()//2))

        tables_rects.append((t, rect, t in used_tables))

    info = font_small.render("Red = In Use (click to release)", True, BLACK)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 380))

    back_btn = draw_button("Back", WIDTH//2 - 150, 500, 300, 60)

    return tables_rects, back_btn

# ===== MAIN LOOP =====
running = True
item_boxes = []
thank_you_start_time = None

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TAKEAWAY NAME TYPING (only when active)
        if current_screen == "takeaway_name" and event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                customer_name = customer_name[:-1]
            elif event.key == pygame.K_RETURN:
                current_screen = "thank_you"
                thank_you_start_time = pygame.time.get_ticks()
                current_order.clear()
            else:
                customer_name += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "main_menu":
                start_btn = draw_button("Start New Order", 350, 300, 300, 70)
                release_btn = draw_button("Release Table", 350, 380, 300, 70)
                quit_btn = draw_button("Quit", 350, 460, 300, 70)

                if start_btn.collidepoint(event.pos):
                    current_screen = "ordering"

                if release_btn.collidepoint(event.pos):
                    current_screen = "release_table"

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
                    current_screen = "complete_review"

            elif current_screen == "order_summary":
                back_btn = draw_order_summary()
                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

            elif current_screen == "complete_review":
                continue_btn, back_btn = draw_complete_order()

                if continue_btn.collidepoint(event.pos):
                    current_screen = "order_type"

                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

            elif current_screen == "order_type":
                dine_rect, take_rect, back_btn = draw_order_type()

                if dine_rect.collidepoint(event.pos):
                    if len(tables_available) == 0:
                        current_screen = "no_tables"
                    else:
                        current_screen = "dine_in"

                if take_rect.collidepoint(event.pos):
                    current_screen = "takeaway_name"
                    # reset input state
                    input_active = False

                if back_btn.collidepoint(event.pos):
                    current_screen = "complete_review"

            elif current_screen == "takeaway_name":
                enter_btn, back_btn = draw_takeaway_name()

                # text box rect (same as in draw_takeaway_name)
                name_box = pygame.Rect(WIDTH//2 - 200, 260, 400, 60)
                if name_box.collidepoint(event.pos):
                    input_active = True

                if enter_btn.collidepoint(event.pos):
                    current_screen = "thank_you"
                    thank_you_start_time = pygame.time.get_ticks()
                    current_order.clear()
                    customer_name = ""
                    input_active = False

                if back_btn.collidepoint(event.pos):
                    current_screen = "order_type"
                    input_active = False

            elif current_screen == "dine_in":
                enter_btn, table_num = draw_dine_in()

                if enter_btn and enter_btn.collidepoint(event.pos):
                    if table_num in tables_available:
                        tables_available.remove(table_num)
                    current_screen = "thank_you"
                    thank_you_start_time = pygame.time.get_ticks()
                    current_order.clear()

            elif current_screen == "no_tables":
                back_btn = draw_no_tables()

                if back_btn.collidepoint(event.pos):
                    current_screen = "order_type"

            elif current_screen == "release_table":
                tables_rects, back_btn = draw_release_table()

                for t, rect, is_used in tables_rects:
                    if rect.collidepoint(event.pos) and is_used:
                        if t not in tables_available:
                            tables_available.append(t)
                            tables_available.sort()

                if back_btn.collidepoint(event.pos):
                    current_screen = "main_menu"

    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
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
        cost_label = font_medium.render(f"Cost: ${total_cost:.2f}", True, BLACK)
        screen.blit(cost_label, (20, HEIGHT - 60))

        draw_button("See Order", 260, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Cancel Order", 480, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Complete Order", 700, HEIGHT - 72, 230, 55, BLUE_DARK)

        if popup_item:
            draw_popup()

    elif current_screen == "order_summary":
        draw_order_summary()

    elif current_screen == "complete_review":
        draw_complete_order()

    elif current_screen == "order_type":
        draw_order_type()

    elif current_screen == "takeaway_name":
        draw_takeaway_name()

    elif current_screen == "dine_in":
        draw_dine_in()

    elif current_screen == "no_tables":
        draw_no_tables()

    elif current_screen == "release_table":
        draw_release_table()

    elif current_screen == "thank_you":
        draw_thank_you()
        if thank_you_start_time and pygame.time.get_ticks() - thank_you_start_time >= 8000:
            current_screen = "main_menu"

    pygame.display.update()

pygame.quit()