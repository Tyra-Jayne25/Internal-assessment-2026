import pygame
import os
pygame.init()

# ===== CONSTANTS =====
# Values define the screen size, colours, and fonts used throughout the program
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

#Fonts used for different text sizes
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

MAX_ITEM_QUANTITY = 10

# ===== MENU =====
# dictionary defining the menu structure, categories, subcategories, items, and prices
MENU = {
    "Beverages": {
        "Cold Drinks": {
            "Iced Coffee": 3.00,
            "Orange Juice": 2.50,
            "Water": 2.75,
            "Smoothie": 4.00,  # Item opens a multi-option popup for smoothie flavours instead of a normal popup
            "Soda": 1.50       # Same here - opens multi-option popup for soda flavours instead of normal popup
        },
        "Hot Drinks": {
            "Espresso": 2.50,
            "Americano": 2.00,
            "Hot Chocolate": 3.00,
            "Flat White": 2.75,
            "Tea": 3.50
        }
    },
    "Food": {
        "Pastries": {
            "Croissant": 2.00,
            "Muffin": 2.50,
            "Sausage Roll": 2.25,
            "Mince and Cheese pie": 3.00,
            "Steak and Cheese Pie": 1.75
        },
        "Meals": {
            "Eggs Benedict": 5.00,
            "Hot Chips": 4.50,
            "Bacon and Eggs": 6.00,
            "Sandwiches": 7.50,
            "Burger": 8.00
        }
    }
}

# ===== SPECIAL OPTIONS FOR SODA & SMOOTHIE =====
# dictionaries store the individual drink options and their prices for the multi-option popups when "Soda" or "Smoothie" is selected from the menu
SODA_OPTIONS = {
    "Coke": 2.50,
    "Fanta": 2.50,
    "L&P": 2.70,
    "Sprite": 2.40
}

SMOOTHIE_OPTIONS = {
    "Banana Smoothie": 4.80,
    "Chocolate Smoothie": 5.00,
    "Strawberry Smoothie": 4.90,
    "Mango Smoothie": 5.20
}

# ===== GLOBAL VARIABLES =====
# These variables track the current state of the ordering system.
current_order = {} 
current_screen = "main_menu"
current_category = None
current_subcategory = None

scroll_y = 0
popup_item = None
popup_qty = 1

# multi-option popup state
# Tracks whether the multi-option popup is open ("Soda", "Smoothie", or None)
multi_popup_type = None  # "Soda" or "Smoothie" or None

# Stores quantities for each drink inside the multi-option popup
soda_quantities = {name: 0 for name in SODA_OPTIONS}
smoothie_quantities = {name: 0 for name in SMOOTHIE_OPTIONS}

customer_name = ""
tables_available = [1,2,3,4,5,6,7,8,9,10]
assigned_table = None

input_active = False
thank_you_start_time = None

# ===== GUI SETUP =====
# initializes the Pygame screen and sets the window caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Ordering System - Version 3.1")

# ===== IMAGE LOADING =====
def load_image(filename, fallback_color, size):
    # Attempts to load an image from the given filename.
    # If the file does not exist, a coloured placeholder box is created instead.
    if os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            img = pygame.transform.scale(img, size)
            return img
        except:
            pass
    # Creates a placeholder image if loading fails
    surf = pygame.Surface(size)
    surf.fill(fallback_color)
    return surf

# ===== LOAD ALL ITEM IMAGES =====
# loads images for all menu items. If the image file is missing, a grey placeholder is used.
iced_coffee_img = load_image("Iced Coffee.png", GREY, (60, 60))
orange_juice_img = load_image("Orange Juice.png", GREY, (60, 60))
water_img = load_image("Water.png", GREY, (60, 60))
smoothie_img = load_image("Smoothie.png", GREY, (60, 60))
soda_img = load_image("Soda.png", GREY, (60, 60))

espresso_img = load_image("Espresso.png", GREY, (60, 60))
americano_img = load_image("Americano.png", GREY, (60, 60))
hot_chocolate_img = load_image("Hot Chocolate.png", GREY, (60, 60))
flat_white_img = load_image("Flat White.png", GREY, (60, 60))
tea_img = load_image("Tea.png", GREY, (60, 60))

croissant_img = load_image("Croissant.png", GREY, (60, 60))
muffin_img = load_image("Muffin.png", GREY, (60, 60))
sausage_roll_img = load_image("Sausage Roll.png", GREY, (60, 60))
mince_and_cheese_pie_img = load_image("Mince and Cheese pie.png", GREY, (60, 60))
steak_and_cheese_pie_img = load_image("Steak and Cheese Pie.png", GREY, (60, 60))

eggs_benedict_img = load_image("Eggs Benedict.png", GREY, (60, 60))
hot_chips_img = load_image("Hot Chips.png", GREY, (60, 60))
bacon_and_eggs_img = load_image("Bacon and Eggs.png", GREY, (60, 60))
sandwiches_img = load_image("Sandwiches.png", GREY, (60, 60))
burger_img = load_image("Burger.png", GREY, (60, 60))

takeaway_img = load_image("Takeaway.png", GREY, (150, 150))
dinein_img = load_image("Dine-In.png", GREY, (150, 150))

# Images for multi-option soda options
coke_img = load_image("Coke.png", GREY, (60, 60))
fanta_img = load_image("Fanta.png", GREY, (60, 60))
lp_img = load_image("L&P.png", GREY, (60, 60))
sprite_img = load_image("Sprite.png", GREY, (60, 60))

# Images for multi-option smoothie options
banana_smoothie_img = load_image("Banana Smoothie.png", GREY, (60, 60))
chocolate_smoothie_img = load_image("Chocolate Smoothie.png", GREY, (60, 60))
strawberry_smoothie_img = load_image("Strawberry Smoothie.png", GREY, (60, 60))
mango_smoothie_img = load_image("Mango Smoothie.png", GREY, (60, 60))

# ===== MAP ITEM NAMES TO IMAGES =====
# A dictionary that allows the program to quickly find the correct image for any item name
ITEM_IMAGES = {
    "Iced Coffee": iced_coffee_img,
    "Orange Juice": orange_juice_img,
    "Water": water_img,
    "Smoothie": smoothie_img,
    "Soda": soda_img,
    "Espresso": espresso_img,
    "Americano": americano_img,
    "Hot Chocolate": hot_chocolate_img,
    "Flat White": flat_white_img,
    "Tea": tea_img,
    "Croissant": croissant_img,
    "Muffin": muffin_img,
    "Sausage Roll": sausage_roll_img,
    "Mince and Cheese pie": mince_and_cheese_pie_img,
    "Steak and Cheese Pie": steak_and_cheese_pie_img,
    "Eggs Benedict": eggs_benedict_img,
    "Hot Chips": hot_chips_img,
    "Bacon and Eggs": bacon_and_eggs_img,
    "Sandwiches": sandwiches_img,
    "Burger": burger_img,
    # multi-option items:
    "Coke": coke_img,
    "Fanta": fanta_img,
    "L&P": lp_img,
    "Sprite": sprite_img,
    "Banana Smoothie": banana_smoothie_img,
    "Chocolate Smoothie": chocolate_smoothie_img,
    "Strawberry Smoothie": strawberry_smoothie_img,
    "Mango Smoothie": mango_smoothie_img
}

# ===== PRICE LOOKUP (INCLUDES SPECIAL DRINKS) =====
# Returns the price of any item,
def get_price(item_name):
    # first search in MENU structure
    # This allows multi-option items to work with the same pricing system.
    for cat in MENU:
        for sub in MENU[cat]:
            if item_name in MENU[cat][sub]:
                return MENU[cat][sub][item_name]
    # then in soda options
    if item_name in SODA_OPTIONS:
        return SODA_OPTIONS[item_name]
    # then in smoothie options
    if item_name in SMOOTHIE_OPTIONS:
        return SMOOTHIE_OPTIONS[item_name]
    return 0.0

# ===== DRAW BUTTON =====
    # Draws a clickable button with centered text.
def draw_button(text, x, y, w, h, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font_medium.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2,
                        y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# ===== SIDEBAR =====
# Displays the buttons for the main categories (Beverages and Food)
# and the subcategory buttons (Cold Drinks, Hot Drinks, etc.)
def draw_sidebar():
    pygame.draw.rect(screen, GREY, (0, 0, 200, HEIGHT))
    
    # Highlight the selected category
    bev_btn = draw_button("Beverages", 20, 80, 160, 60,
                          BLUE_DARK if current_category == "Beverages" else BLUE)
    food_btn = draw_button("Food", 20, 160, 160, 60,
                           BLUE_DARK if current_category == "Food" else BLUE)
    
    # Draw subcategory buttons only if a category is selected
    sub_buttons = []
    if current_category:
        x = 230
        y = 80
        for sub in MENU[current_category]:
            rect = draw_button(sub, x, y, 180, 50, DARK_GREY)
            sub_buttons.append((sub, rect))
            x += 200

    return bev_btn, food_btn, sub_buttons

# ===== ITEM LIST WITH SCROLLING =====
# Draws the list of items for the selected subcategory.
# Supports scrolling using scroll_y to move the grid up/down.
def draw_item_grid():
    global scroll_y

    if not current_subcategory:
        return []

    items = MENU[current_category][current_subcategory]
    item_boxes = []

    x = 230
    y_start = 160
    y = y_start + scroll_y

    # Calculate scrolling limits so items don't scroll too far
    total_height = len(items) * 110
    visible_bottom = HEIGHT - 120
    min_scroll = min(0, visible_bottom - (y_start + total_height))

    scroll_y = max(min_scroll, min(0, scroll_y))
    y = y_start + scroll_y

    # Clip drawing area so items don't overlap top/bottom bars
    clip_rect = pygame.Rect(200, 140, WIDTH - 200, HEIGHT - 230)
    screen.set_clip(clip_rect)

    # Draw each item box
    for item, price in items.items():
        box = pygame.Rect(x, y, 500, 90)
        pygame.draw.rect(screen, LIGHT_GREY, box)

        img = ITEM_IMAGES.get(item, load_image(f"{item}.png", GREY, (60, 60)))
        screen.blit(img, (x + 10, y + 15))
        screen.blit(font_small.render(item, True, BLACK), (x + 90, y + 15))
        screen.blit(font_small.render(f"${price:.2f}", True, BLACK), (x + 90, y + 50))

        item_boxes.append((item, box))
        y += 110

    screen.set_clip(None)
    return item_boxes

# ===== POPUP WINDOW (SINGLE ITEM) =====
# This function draws the popup window for normal items (NOT Soda or Smoothie).
# It shows the item image, price, quantity buttons, and an "Add to Order" button.
def draw_popup():
    global popup_qty

    # Dark transparent overlay to block background clicks
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Main popup box
    popup = pygame.Rect(250, 120, 500, 400)
    pygame.draw.rect(screen, WHITE, popup)

    # Close button (X)
    close_btn = pygame.Rect(690, 130, 40, 40)
    pygame.draw.rect(screen, RED, close_btn)
    screen.blit(font_medium.render("X", True, WHITE), (701, 138))

    # Item name
    name_label = font_medium.render(popup_item, True, BLACK)
    screen.blit(name_label, (250 + (500 - name_label.get_width()) // 2, 150))

    # Item image
    img_x = 250 + (500 - 200) // 2
    popup_img = load_image(f"{popup_item}.png", GREY, (200, 150))
    screen.blit(popup_img, (img_x, 200))

    # Item price
    price = get_price(popup_item)
    price_label = font_small.render(f"Price: ${price:.2f}", True, BLACK)
    screen.blit(price_label, (250 + (500 - price_label.get_width()) // 2, 360))

    # Quantity buttons
    minus_btn = pygame.Rect(380, 390, 40, 40)
    plus_btn = pygame.Rect(580, 390, 40, 40)
    pygame.draw.rect(screen, RED, minus_btn)
    pygame.draw.rect(screen, GREEN, plus_btn)

    # Quantity display
    qty_label = font_medium.render(str(popup_qty), True, BLACK)
    screen.blit(qty_label, (250 + (500 - qty_label.get_width()) // 2, 395))

    # Minus and Plus signs for quantity buttons
    screen.blit(font_medium.render("-", True, WHITE), (394, 394))
    screen.blit(font_medium.render("+", True, WHITE), (592, 394))

    # Add to order button
    add_btn = draw_button("Add to Order", 350, 450, 300, 50, BLUE_DARK)

    return close_btn, minus_btn, plus_btn, add_btn

# ===== MULTI-OPTION POPUP (SODA / SMOOTHIE) =====
def draw_multi_popup():
# This function draws the special popup for Soda and Smoothie.
# It displays multiple drink options at once, each with its own image, price, and quantity selector.

    # Dark overlay to block background clicks
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Main popup box
    popup = pygame.Rect(200, 80, 600, 480)
    pygame.draw.rect(screen, WHITE, popup)

    # Close button (X)
    close_btn = pygame.Rect(popup.right - 50, popup.top + 10, 40, 40)
    pygame.draw.rect(screen, RED, close_btn)
    screen.blit(font_medium.render("X", True, WHITE), (close_btn.x + 10, close_btn.y + 5))

    # Determine which options to show based on whether it's Soda or Smoothie
    if multi_popup_type == "Soda":
        title_text = "Sodas"
        options = SODA_OPTIONS
        quantities = soda_quantities
    else:
        title_text = "Smoothies"
        options = SMOOTHIE_OPTIONS
        quantities = smoothie_quantities

    # Popup title
    title = font_medium.render(title_text, True, BLACK)
    screen.blit(title, (popup.centerx - title.get_width()//2, popup.top + 20))

    # Draw each drink option in the popup
    item_rows = {}
    start_y = popup.top + 80
    row_height = 90

    for i, (name, price) in enumerate(options.items()):
        # Draw background for the row
        row_y = start_y + i * row_height
        row_rect = pygame.Rect(popup.left + 20, row_y, popup.width - 40, row_height - 10)
        pygame.draw.rect(screen, LIGHT_GREY, row_rect)
        
        # Draw the drink image
        img = ITEM_IMAGES.get(name, load_image(f"{name}.png", GREY, (60, 60)))
        screen.blit(img, (row_rect.x + 10, row_rect.y + 10))

        # Draw the drink name and price
        name_label = font_small.render(name, True, BLACK)
        screen.blit(name_label, (row_rect.x + 90, row_rect.y + 10))

        # Draw price below the name
        price_label = font_small.render(f"${price:.2f}", True, BLACK)
        screen.blit(price_label, (row_rect.x + 90, row_rect.y + 40))

        # Draw quantity buttons and display
        minus_btn = pygame.Rect(row_rect.right - 150, row_rect.y + 20, 30, 30)
        plus_btn = pygame.Rect(row_rect.right - 50, row_rect.y + 20, 30, 30)
        qty_val = quantities[name]
        qty_label = font_small.render(str(qty_val), True, BLACK)

        # Draw the minus and plus buttons, and the quantity in between
        pygame.draw.rect(screen, RED, minus_btn)
        pygame.draw.rect(screen, GREEN, plus_btn)
        screen.blit(font_small.render("-", True, WHITE), (minus_btn.x + 9, minus_btn.y + 3))
        screen.blit(font_small.render("+", True, WHITE), (plus_btn.x + 9, plus_btn.y + 3))
        screen.blit(qty_label, (row_rect.right - 100 - qty_label.get_width()//2, row_rect.y + 25))
        
        # Store the button rects for this item so we can check clicks later
        item_rows[name] = (minus_btn, plus_btn)
    
    # Add to order button
    add_btn = draw_button("Add to Order", popup.centerx - 150, popup.bottom - 70, 300, 50, BLUE_DARK)

    return close_btn, add_btn, item_rows

# ===== ORDER SUMMARY (RESTORED SPACING) =====
# This screen shows all items currently in the order.
# Items are displayed in two columns, with delete buttons next to each item.
def draw_order_summary():
    screen.fill(WHITE)

    # Draw header
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    screen.blit(font_medium.render("ORDER", True, WHITE), (20, 10))

    # Get list of items with quantity > 0
    items = [(item, qty) for item, qty in current_order.items() if qty > 0]

    col1_x = 80
    col2_x = 500
    y = 140
    count = 0

    delete_buttons = []

    # Draw each item in the order with its quantity and total price, and a delete button next to it
    for item, qty in items:
        price = get_price(item)

        x = col1_x if count % 2 == 0 else col2_x

        # Item text
        text_surf = font_small.render(f"{item} x{qty} - ${price * qty:.2f}", True, BLACK)
        screen.blit(text_surf, (x, y))
        
        # Delete button
        del_btn = pygame.Rect(x + 260, y - 2, 90, 32)
        pygame.draw.rect(screen, RED, del_btn)
        del_label = font_small.render("Delete", True, WHITE)
        screen.blit(del_label, (del_btn.x + (del_btn.width - del_label.get_width()) // 2,
                                del_btn.y + (del_btn.height - del_label.get_height()) // 2))

        delete_buttons.append((item, del_btn))
        
        # Move to next column after every 2 items
        if count % 2 == 1:
            y += 40

        count += 1
    
    # Calculate and display total cost at the bottom
    total_cost = sum(get_price(item) * qty for item, qty in current_order.items() if qty > 0)
    screen.blit(font_medium.render(f"Total: ${total_cost:.2f}", True, BLACK), (60, 570))

    # Continue and Back buttons
    back_btn = draw_button("Back", 800, 560, 150, 50)

    return back_btn, delete_buttons

# ===== THANK YOU SCREEN FOR TAKEAWAY =====
# This screen appears after a takeaway order is completed.
# It shows the customer's name, their order, and the total cost.
def draw_thank_you_takeaway():
    screen.fill(WHITE)
    
    # Draw header
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = font_large.render("Cafe Name", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Draw the light grey panel for the order summary
    panel_w = 600
    panel_h = 400
    panel_x = WIDTH//2 - panel_w//2
    panel_y = 120

    pygame.draw.rect(screen, LIGHT_GREY, (panel_x, panel_y, panel_w, panel_h))

    # Display the customer's name at the top of the panel
    name_label = font_medium.render(f"Name: {customer_name}", True, BLACK)
    screen.blit(name_label, (panel_x + 20, panel_y + 20))

    # Draw a line to separate the name from the order details
    pygame.draw.line(screen, BLACK, (panel_x + 20, panel_y + 60), (panel_x + panel_w - 20, panel_y + 60), 2)

    # List each item in the order with its quantity and total price, spaced out vertically
    y = panel_y + 80
    for item, qty in current_order.items():
        if qty > 0:
            price = get_price(item)
            line = font_small.render(f"{qty} {item}   ${price * qty:.2f}", True, BLACK)
            screen.blit(line, (panel_x + 20, y))
            y += 35
    
    # Calculate and display the total cost at the bottom of the panel
    total_cost = sum(get_price(item) * qty for item, qty in current_order.items() if qty > 0)
    total_label = font_medium.render(f"Total cost: ${total_cost:.2f}", True, BLACK)
    screen.blit(total_label, (panel_x + 20, y + 20))

    # Display a thank you message below the panel
    thanks = font_medium.render("Thank you for ordering at our Cafe!", True, BLACK)
    screen.blit(thanks, (WIDTH//2 - thanks.get_width()//2, panel_y + panel_h + 30))

# ===== THANK YOU SCREEN FOR DINE-IN (LIGHT BACKGROUND PANEL) =====

def draw_thank_you_dinein():
    # This screen appears after a dine-in order is completed.
    # It shows the assigned table number, the order, and the total cost.

    screen.fill(WHITE)

    # Draw header
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = font_large.render("Cafe Name", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Draw the light grey panel for the order summary
    panel_w = 600
    panel_h = 400
    panel_x = WIDTH//2 - panel_w//2
    panel_y = 120
    pygame.draw.rect(screen, LIGHT_GREY, (panel_x, panel_y, panel_w, panel_h))

    # Display the assigned table number at the top of the panel
    table_label = font_medium.render(f"Table no.: {assigned_table}", True, BLACK)
    screen.blit(table_label, (panel_x + 20, panel_y + 20))

    # Draw a line to separate the table number from the order details
    pygame.draw.line(screen, BLACK, (panel_x + 20, panel_y + 60), (panel_x + panel_w - 20, panel_y + 60), 2)

    # List each item in the order with its quantity and total price, spaced out vertically
    y = panel_y + 80
    for item, qty in current_order.items():
        if qty > 0:
            price = get_price(item)
            line = font_small.render(f"{qty} {item}   ${price * qty:.2f}", True, BLACK)
            screen.blit(line, (panel_x + 20, y))
            y += 35
    # Calculate and display the total cost at the bottom of the panel
    total_cost = sum(get_price(item) * qty for item, qty in current_order.items() if qty > 0)
    total_label = font_medium.render(f"Total cost: ${total_cost:.2f}", True, BLACK)
    screen.blit(total_label, (panel_x + 20, y + 20))
    
    # Display a thank you message below the panel
    thanks = font_medium.render("Thank you for ordering at our Cafe!", True, BLACK)
    screen.blit(thanks, (WIDTH//2 - thanks.get_width()//2, panel_y + panel_h + 30))

# ===== UPDATED ORDER TYPE SCREEN =====
def draw_order_type():
    # This screen lets the user choose between Takeaway or Dine‑In.
    # It appears after the user clicks "Complete Order".
    screen.fill(WHITE)

    # Draw header
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = font_medium.render("ORDER TYPE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Draw the Takeaway option box
    take_rect = pygame.Rect(200, 200, 250, 250)
    pygame.draw.rect(screen, LIGHT_GREY, take_rect)
    screen.blit(takeaway_img, (take_rect.x + 50, take_rect.y + 20))

    # Label for Takeaway option
    take_label = font_medium.render("Takeaway", True, BLACK)
    screen.blit(take_label, (take_rect.centerx - take_label.get_width()//2,
                             take_rect.y + 190))

    # Draw the Dine-In option box
    dine_rect = pygame.Rect(550, 200, 250, 250)
    pygame.draw.rect(screen, LIGHT_GREY, dine_rect)
    screen.blit(dinein_img, (dine_rect.x + 50, dine_rect.y + 20))

    # Label for Dine-In option
    dine_label = font_medium.render("Dine-In", True, BLACK)
    screen.blit(dine_label, (dine_rect.centerx - dine_label.get_width()//2,
                             dine_rect.y + 190))

    back_btn = draw_button("Back", WIDTH//2 - 150, 500, 300, 60)

    return dine_rect, take_rect, back_btn

# ===== UPDATED TAKEAWAY SCREEN =====
# This screen appears after the user selects "Takeaway" as their order type.
def draw_takeaway_name():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    
    # Draw header
    title = font_medium.render("TAKEAWAY", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Prompt for the user to enter their name, with a text box and an "Enter" button
    prompt = font_medium.render("Enter your name:", True, BLACK)
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 200))

    # Draw the text box for name input
    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH//2 - 200, 260, 400, 60))
    name_text = font_medium.render(customer_name, True, BLACK)
    screen.blit(name_text, (WIDTH//2 - 190, 270))

    # Draw the Enter and Back buttons
    enter_btn = draw_button("Enter", WIDTH//2 - 150, 350, 300, 70)
    back_btn = draw_button("Back", WIDTH//2 - 150, 450, 300, 70)

    return enter_btn, back_btn

# ===== UPDATED DINE-IN SCREEN =====
def draw_dine_in():
# This screen appears after the user selects "Dine-In" as their order type.
# It shows the assigned table number and an "Enter" button to proceed to the order summary.
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    
    # Draw header
    title = font_medium.render("DINE-IN", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    if len(tables_available) == 0:
        return None, None

    # Assign the first available table to the customer
    table_num = tables_available[0]

    # Display the assigned table number in the center of the screen, with an "Enter" button below it
    label = font_medium.render("Your table number is:", True, BLACK)
    screen.blit(label, (WIDTH//2 - label.get_width()//2, 200))

    # Draw a light grey box around the table number to make it stand out
    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH//2 - 75, 260, 150, 100))
    num = font_large.render(str(table_num), True, BLACK)
    screen.blit(num, (WIDTH//2 - num.get_width()//2, 280))
    
    # Draw the Enter button to proceed to the order summary
    enter_btn = draw_button("Enter", WIDTH//2 - 150, 450, 300, 70)
    return enter_btn, table_num

# ===== UPDATED REVIEW ORDER SCREEN (RESTORED SPACING) =====
def draw_complete_order():
# This screen shows a summary of the current order before finalizing.
# Items are displayed in two columns, with delete buttons next to each item, and the total cost at the bottom.
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    # Draw header
    title = font_medium.render("REVIEW ORDER", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    items = [(item, qty) for item, qty in current_order.items() if qty > 0]

    # Display items in two columns with restored spacing, and add delete buttons next to each item
    col1_x = 80
    col2_x = 500
    y = 140
    count = 0

    delete_buttons = []
    
    # Loop through each item in the order and display it with its quantity and total price, along with a delete button.
    for item, qty in items:
        price = get_price(item)

        x = col1_x if count % 2 == 0 else col2_x
        text_surf = font_small.render(f"{item} x{qty} - ${price * qty:.2f}", True, BLACK)
        screen.blit(text_surf, (x, y))

        # Draw the delete button next to each item
        del_btn = pygame.Rect(x + 260, y - 2, 90, 32)
        pygame.draw.rect(screen, RED, del_btn)
        del_label = font_small.render("Delete", True, WHITE)
        screen.blit(del_label, (del_btn.x + (del_btn.width - del_label.get_width()) // 2,
                                del_btn.y + (del_btn.height - del_label.get_height()) // 2))

        delete_buttons.append((item, del_btn))

        if count % 2 == 1:
            y += 40

        count += 1

    # Calculate and display the total cost at the bottom of the screen
    total_cost = sum(get_price(item) * qty for item, qty in current_order.items() if qty > 0)
    total_label = font_medium.render(f"Total: ${total_cost:.2f}", True, BLACK)
    screen.blit(total_label, (60, 570))
    
    # Draw the Continue button to finalize the order, and a Back button to return to the ordering screen
    continue_btn = draw_button("Continue", WIDTH//2 - 100, 560, 200, 50)
    back_btn = draw_button("Back", WIDTH - 200, 560, 150, 50)

    return continue_btn, back_btn, delete_buttons

# ===== NO TABLES SCREEN =====
def draw_no_tables():
# This screen appears if the user selects "Dine-In" but there are no tables available.
# It informs the user that there are no tables and provides a "Back" button to return to the order type selection screen.
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    # Draw header
    title = font_medium.render("NO TABLES AVAILABLE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Display a message in the center of the screen informing the user that there are no tables available, and to wait for the next available table.
    msg = font_medium.render("Sorry, no tables available. Please wait for the next available table.", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))

    # Draw a "Back" button to return to the order type selection screen
    back_btn = draw_button("Back", WIDTH//2 - 150, 450, 300, 70)
    return back_btn

# ===== RELEASE TABLE SCREEN =====
def draw_release_table():
# This screen allows the user to release a table that is currently in use.
# It shows all tables, highlighting those that are currently occupied, and allows the user to click on an occupied table to release it.
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    # Draw header
    title = font_medium.render("RELEASE TABLE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    # Draw all tables as rectangles, highlighting those that are currently in use (not in tables_available).
    tables_rects = []
    all_tables = list(range(1, 11))
    used_tables = [t for t in all_tables if t not in tables_available]
    
    # Calculate positions for the table rectangles in a grid layout (2 rows of 5 tables)
    start_x = 200
    start_y = 150
    w, h = 100, 80
    gap_x = 40
    gap_y = 40

    # Loop through all tables and draw them in a grid, coloring them red if they are in use and grey if they are available. Store the rects for click detection.
    for i, t in enumerate(all_tables):
        row = i // 5
        col = i % 5
        x = start_x + col * (w + gap_x)
        y = start_y + row * (h + gap_y)

        color = RED if t in used_tables else GREY
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, rect)
        
        # Draw the table number in the center of the rectangle, using white text for occupied tables and black text for available tables to ensure readability.
        label = font_medium.render(str(t), True, WHITE if t in used_tables else BLACK)
        screen.blit(label, (rect.centerx - label.get_width()//2,
                            rect.centery - label.get_height()//2))

        tables_rects.append((t, rect, t in used_tables))
    
    # Display instructions below the tables, explaining that red tables are currently in use and can be clicked to release them.
    info = font_small.render("Red = In Use (click to release)", True, BLACK)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 380))

    # Draw a "Back" button to return to the main menu
    back_btn = draw_button("Back", WIDTH//2 - 150, 500, 300, 60)

    return tables_rects, back_btn

# ===== RESET ORDER STATE =====
def reset_order_state():
# This function resets ALL variables so a new order can start fresh.
    global current_order, current_category, current_subcategory
    global scroll_y, popup_item, popup_qty
    global customer_name, assigned_table, input_active, thank_you_start_time
    global multi_popup_type, soda_quantities, smoothie_quantities

    current_order = {}
    current_category = None
    current_subcategory = None
    scroll_y = 0
    popup_item = None
    popup_qty = 1
    customer_name = ""
    assigned_table = None
    input_active = False
    thank_you_start_time = None

    # Reset multi-option popup state
    multi_popup_type = None
    soda_quantities = {name: 0 for name in SODA_OPTIONS}
    smoothie_quantities = {name: 0 for name in SMOOTHIE_OPTIONS}

# ===== MAIN LOOP =====
running = True
item_boxes = []

while running:
    # Clear screen each frame
    screen.fill(WHITE)
 
    # Handle all events (mouse clicks, keyboard input, etc.)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
       
        # Handle scrolling in item grid
        if current_screen == "ordering" and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll_y += 30
            elif event.button == 5:
                scroll_y -= 30
            if event.button in (4, 5):
                continue

        # Handle typing name in takeaway screen
        if current_screen == "takeaway_name" and event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                customer_name = customer_name[:-1]
            elif event.key == pygame.K_RETURN:
                input_active = False
            else:
                customer_name += event.unicode

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # MAIN MENU SCREEN
            if current_screen == "main_menu":
                start_btn = pygame.Rect(350, 300, 300, 70)
                release_btn = pygame.Rect(350, 380, 300, 70)
                quit_btn = pygame.Rect(350, 460, 300, 70)

                if start_btn.collidepoint(event.pos):
                    reset_order_state()
                    current_screen = "ordering"

                if release_btn.collidepoint(event.pos):
                    current_screen = "release_table"

                if quit_btn.collidepoint(event.pos):
                    running = False

            # ORDERING SCREEN
            elif current_screen == "ordering":
                
                # Draw sidebar buttons and detect clicks
                bev_btn, food_btn, sub_btns = draw_sidebar()

                if bev_btn.collidepoint(event.pos):
                    current_category = "Beverages"
                    current_subcategory = None
                    scroll_y = 0

                if food_btn.collidepoint(event.pos):
                    current_category = "Food"
                    current_subcategory = None
                    scroll_y = 0
                
                # Subcategory buttons
                for sub, rect in sub_btns:
                    if rect.collidepoint(event.pos):
                        current_subcategory = sub
                        scroll_y = 0

                # handle multi-option popup first
                if multi_popup_type is not None:
                    close_btn, add_btn, item_rows = draw_multi_popup()
                    
                    # close button for multi-option popup
                    if close_btn.collidepoint(event.pos):
                        multi_popup_type = None
                        continue

                    # per-item +/- buttons
                    if multi_popup_type == "Soda":
                        quantities = soda_quantities
                        options = SODA_OPTIONS
                    else:
                        quantities = smoothie_quantities
                        options = SMOOTHIE_OPTIONS

                    # check if any of the +/- buttons were clicked for each item in the multi-option popup
                    clicked_any = False
                    for name, (minus_btn, plus_btn) in item_rows.items():
                        if minus_btn.collidepoint(event.pos):
                            quantities[name] = max(0, quantities[name] - 1)
                            clicked_any = True
                            break
                        if plus_btn.collidepoint(event.pos):
                            quantities[name] = min(MAX_ITEM_QUANTITY, quantities[name] + 1)
                            clicked_any = True
                            break

                    if clicked_any:
                        continue
                    
                    # add to order button for multi-option popup
                    if add_btn.collidepoint(event.pos):
                        for name, qty in quantities.items():
                            if qty > 0:
                                current_order[name] = min(
                                    MAX_ITEM_QUANTITY,
                                    current_order.get(name, 0) + qty
                                )
                        multi_popup_type = None
                        # reset quantities after adding
                        soda_quantities = {n: 0 for n in SODA_OPTIONS}
                        smoothie_quantities = {n: 0 for n in SMOOTHIE_OPTIONS}
                        continue

                    # block background clicks
                    continue

                # handle single-item popup
                if popup_item is not None:
                    close_btn, minus_btn, plus_btn, add_btn = draw_popup()

                    # check if any of the popup buttons were clicked
                    if close_btn.collidepoint(event.pos):
                        popup_item = None
                        continue

                    # check minus, plus, and add buttons for single-item popup
                    if minus_btn.collidepoint(event.pos):
                        popup_qty = max(1, popup_qty - 1)
                        continue

                    # check plus button for single-item popup
                    if plus_btn.collidepoint(event.pos):
                        popup_qty = min(MAX_ITEM_QUANTITY, popup_qty + 1)
                        continue

                    # check add to order button for single-item popup
                    if add_btn.collidepoint(event.pos):
                        current_order[popup_item] = min(
                            MAX_ITEM_QUANTITY,
                            current_order.get(popup_item, 0) + popup_qty
                        )
                        popup_item = None
                        continue

                    continue

                # block clicks on top and bottom bars from hitting items
                y_click = event.pos[1]
                in_content_area = (y_click >= 160) and (y_click <= HEIGHT - 120)

                # If no popups are open and the click is within the content area, check if an item was clicked to open its popup.
                if popup_item is None and multi_popup_type is None and current_subcategory and in_content_area:
                    for item, rect in item_boxes:
                        if rect.collidepoint(event.pos):
                            if item == "Soda":
                                multi_popup_type = "Soda"
                                soda_quantities = {n: 0 for n in SODA_OPTIONS}
                            elif item == "Smoothie":
                                multi_popup_type = "Smoothie"
                                smoothie_quantities = {n: 0 for n in SMOOTHIE_OPTIONS}
                            else:
                                popup_item = item
                                popup_qty = 1
                            break

                # Only open a popup if the click was within the content area (not on the top or bottom bars)
                see_btn = pygame.Rect(260, HEIGHT - 72, 200, 55)
                cancel_btn = pygame.Rect(480, HEIGHT - 72, 200, 55)
                complete_btn = pygame.Rect(700, HEIGHT - 72, 230, 55)

                # Check if the "See Order", "Cancel Order", or "Complete Order" buttons were clicked, and navigate to the appropriate screen or reset state.
                if see_btn.collidepoint(event.pos):
                    current_screen = "order_summary"

                # Check if the "Cancel Order" button was clicked, and if so, reset the order state and return to the main menu.
                if cancel_btn.collidepoint(event.pos):
                    reset_order_state()
                    current_screen = "main_menu"
                
                # Check if the "Complete Order" button was clicked, and if so, navigate to the complete review screen.
                if complete_btn.collidepoint(event.pos):
                    current_screen = "complete_review"

            # ORDER SUMMARY
            elif current_screen == "order_summary":
                back_btn, delete_buttons = draw_order_summary()

                # Check if any delete buttons were clicked, and if so, remove that item from the current order.
                for item, btn in delete_buttons:
                    if btn.collidepoint(event.pos):
                        if item in current_order:
                            del current_order[item]
                        break

                # Check if the Back button was clicked, and if so, return to the ordering screen.
                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

            # COMPLETE REVIEW
            elif current_screen == "complete_review":
                continue_btn, back_btn, delete_buttons = draw_complete_order()

                # Check if any delete buttons were clicked, and if so, remove that item from the current order.
                for item, btn in delete_buttons:
                    if btn.collidepoint(event.pos):
                        if item in current_order:
                            del current_order[item]
                        break
                
                # Check if the Continue button was clicked, and if so, navigate to the order type selection screen.
                if continue_btn.collidepoint(event.pos):
                    current_screen = "order_type" 
                
                # Check if the Back button was clicked, and if so, return to the ordering screen.
                if back_btn.collidepoint(event.pos):
                    current_screen = "ordering"

            # ORDER TYPE
            elif current_screen == "order_type":
                dine_rect, take_rect, back_btn = draw_order_type()

                if dine_rect.collidepoint(event.pos):
                    if len(tables_available) == 0:
                        current_screen = "no_tables"
                    else:
                        current_screen = "dine_in"

                # Check if the Takeaway option was clicked, and if so, navigate to the takeaway name input screen.
                if take_rect.collidepoint(event.pos):
                    current_screen = "takeaway_name"
                    input_active = False
                
                # Check if the Back button was clicked, and if so, return to the complete review screen.
                if back_btn.collidepoint(event.pos):
                    current_screen = "complete_review"

            # TAKEAWAY NAME
            elif current_screen == "takeaway_name":
                enter_btn, back_btn = draw_takeaway_name()

                # Check if the text box was clicked, and if so, activate it for typing.
                name_box = pygame.Rect(WIDTH//2 - 200, 260, 400, 60)
                if name_box.collidepoint(event.pos):
                    input_active = True

                # Check if the Enter button was clicked, and if so, navigate to the thank you screen for takeaway orders.
                if enter_btn.collidepoint(event.pos):
                    current_screen = "thank_you_takeaway"
                    thank_you_start_time = pygame.time.get_ticks()
                    input_active = False

                # Check if the Back button was clicked, and if so, return to the order type selection screen.
                if back_btn.collidepoint(event.pos):
                    current_screen = "order_type"
                    input_active = False

            # DINE IN
            elif current_screen == "dine_in":
                enter_btn, table_num = draw_dine_in()

                # Check if the Enter button was clicked, and if so, assign the table to the customer (removing it from the available tables list) and navigate to the thank you screen for dine-in orders.
                if enter_btn and enter_btn.collidepoint(event.pos):
                    if table_num in tables_available:
                        tables_available.remove(table_num)
                        assigned_table = table_num
                    current_screen = "thank_you_dinein"
                    thank_you_start_time = pygame.time.get_ticks()

            # NO TABLES
            elif current_screen == "no_tables":
                back_btn = draw_no_tables()

                if back_btn.collidepoint(event.pos):
                    current_screen = "order_type"

            # RELEASE TABLE
            elif current_screen == "release_table":
                tables_rects, back_btn = draw_release_table()

                for t, rect, is_used in tables_rects:
                    if rect.collidepoint(event.pos) and is_used:
                        if t not in tables_available:
                            tables_available.append(t)
                            tables_available.sort()

                if back_btn.collidepoint(event.pos):
                    current_screen = "main_menu"

    # ===== SCREEN DRAWING =====
# Based on the current screen state, draw the appropriate UI elements and content for that screen.
    if current_screen == "main_menu":
        title = font_large.render("Cafe Ordering System", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        draw_button("Start New Order", 350, 300, 300, 70)
        draw_button("Release Table", 350, 380, 300, 70)
        draw_button("Quit", 350, 460, 300, 70)

    elif current_screen == "ordering":
        bev_btn, food_btn, sub_btns = draw_sidebar()

        item_boxes = draw_item_grid()

        pygame.draw.rect(screen, BLUE, (200, 0, WIDTH - 200, 140))

        # Draw header
        x = 230
        y = 80
        sub_btns = []
        if current_category:
            for sub in MENU[current_category]:
                rect = draw_button(sub, x, y, 180, 50, DARK_GREY)
                sub_btns.append((sub, rect))
                x += 200

        pygame.draw.rect(screen, BLUE, (200, HEIGHT - 90, WIDTH - 200, 90))

        # Calculate and display the total cost of the current order at the bottom of the screen, above the buttons.
        total_cost = sum(get_price(item) * qty for item, qty in current_order.items() if qty > 0)
        cost_label = font_medium.render(f"Cost: ${total_cost:.2f}", True, BLACK)
        screen.blit(cost_label, (20, HEIGHT - 60))

        # Draw the "See Order", "Cancel Order", and "Complete Order" buttons at the bottom of the screen.
        draw_button("See Order", 260, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Cancel Order", 480, HEIGHT - 72, 200, 55, BLUE_DARK)
        draw_button("Complete Order", 700, HEIGHT - 72, 230, 55, BLUE_DARK)

        # If a popup is open, draw it on top of the ordering screen.
        if multi_popup_type:
            draw_multi_popup()
        elif popup_item:
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

    elif current_screen == "thank_you_takeaway":
        draw_thank_you_takeaway()
        if thank_you_start_time and pygame.time.get_ticks() - thank_you_start_time >= 8000:
            reset_order_state()
            current_screen = "main_menu"

    elif current_screen == "thank_you_dinein":
        draw_thank_you_dinein()
        if thank_you_start_time and pygame.time.get_ticks() - thank_you_start_time >= 8000:
            reset_order_state()
            current_screen = "main_menu"

    pygame.display.update()

pygame.quit()