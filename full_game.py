from saloon import run_saloon_game
from salon import run_salon_game
from work import run_work_game
from bedroom import run_bedroom_game
from happiness import draw_happiness_meter
import pygame
from store import run_store
import math

def fade_to_black(screen, clock, background, speed=5):
    """
    Fades the screen to black
    par background: draws the current frame before fading starts to we fade over the real image .
    par speed: customize the speed of the fading
    """
    fade_surface = pygame.Surface(screen.get_size()).convert()
    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 256, speed):
        screen.blit(background, (0, 0))  # redraw the current background/scene
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def calculate_miles_traveled(current_screen, previous_screen):
    '''
    takes in the two screens and uses a function to calculate distance in MILES between them (usa)
    '''
    miles_traveled = 0
    locations = {"salon": [150,500],
                 "saloon": [550,350],
                 "store": [750,600],
                 "work": [850,475],
                 "bedroom": [250,340]}
    loc1 = locations[previous_screen]
    loc2 = locations[current_screen]

    miles_traveled = math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    return int(round(miles_traveled*10,0))


def draw_dotted_line(surface, color, start_loc, end_loc, width=2, dash_length=10, space_length=5):
    locations = {"salon": [150, 500],
                 "saloon": [550, 350],
                 "store": [750, 600],
                 "work": [850, 475],
                 "bedroom": [250, 340]}
    start_pos = locations[start_loc]
    end_pos = locations[end_loc]
    if start_pos == end_pos:
        return 0
    else:
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx ** 2 + dy ** 2) ** 0.5
        steps = int(distance // (dash_length + space_length))

        for i in range(steps + 1):
            start_x = x1 + (dx / distance) * (i * (dash_length + space_length))
            start_y = y1 + (dy / distance) * (i * (dash_length + space_length))
            end_x = x1 + (dx / distance) * (i * (dash_length + space_length) + dash_length)
            end_y = y1 + (dy / distance) * (i * (dash_length + space_length) + dash_length)

            # Clamp final segment so it doesn’t overshoot
            if (end_x - x1) * dx + (end_y - y1) * dy > dx ** 2 + dy ** 2:
                end_x, end_y = x2, y2

            pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)

def draw_face(miles_traveled, face_rect):
    if miles_traveled < 1000:
        face = pygame.image.load(f"data/image/face{0}.png")
    elif 1000 <= miles_traveled < 10000:
        face = pygame.image.load(f"data/image/face{1}.png")
    elif 10000 <= miles_traveled < 20000:
        face = pygame.image.load(f"data/image/face{2}.png")
    elif 20000 <= miles_traveled < 30000:
        face = pygame.image.load(f"data/image/face{3}.png")
    elif 30000 <= miles_traveled < 40000:
        face = pygame.image.load(f"data/image/face{4}.png")
    elif 40000 <= miles_traveled:
        face = pygame.image.load(f"data/image/face{5}.png")
    face = pygame.transform.scale(face, (50, 50))
    screen.blit(face, face_rect)


# --- Initialize Game ---
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Prumpi World")
clock = pygame.time.Clock()

# --- Set Font and Button Colors  ---
font = pygame.font.SysFont("comic_sansms", 32)
button_color = (255, 225, 125)
button_text_color = (24, 100, 24)


num_coins = 0
# Accessories
bow = False
gem = False
backpack = False
hat = False
heels = False
labubu = False

# ---Quests---
# Work
work_complete = True
work_first_open = True
work_first_complete = True
num_customers = 0
num_rows = 0
hydration = 0

# Salon
salon_complete = True
salon_first_open = True
salon_first_complete = True
num_dinners = 0
num_desserts = 0
num_twerks = 0
num_happiness = 0

# Saloon
saloon_complete = True
saloon_first_open = True
saloon_first_complete = True
num_aces = 0
num_spitballs = 0
num_beers = 0

# Bedroom
bedroom_complete = False
bedroom_first_open = True
bedroom_first_complete = True
web_coins = 0
num_reads = 0

# Happiness
happiness = 0
HAPPINESS_MAX = 30


# Carbon footprint stuff
miles_traveled = 0
connections = []
current_world = None
last_world = None
button_rect_miles = pygame.Rect(600, 20, 200, 60)
button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True, button_color)
button_rect_carbon = pygame.Rect(600, 70, 200, 60)
button_text_carbon = font.render(f"Carbon Footprint:", True, button_color)
face_rect = pygame.Rect(875, 70, 50, 50)



# --- Load images ---
background = pygame.image.load("data/image/prumpi_world.png")
title_image = pygame.image.load('data/image/world_title.png')
pin = pygame.image.load('data/image/pin.png')
volume_on_img = pygame.image.load("data/image/volume_on.png")
volume_off_img = pygame.image.load("data/image/volume_off.png")
coin_img = pygame.image.load("data/image/coin.png")
lock = pygame.image.load("data/image/lock.png")

# --- Rescale images ---
background = pygame.transform.scale(background, (1000, 700))
title_image = pygame.transform.scale(title_image, (500, 300))
pin = pygame.transform.scale(pin, (100,100))
coin_img = pygame.transform.scale(coin_img, (80, 80))
lock = pygame.transform.scale(lock, (50,50))

# --- Create buttons ---
button_rect_begin = pygame.Rect(400, 500, 200, 60)
button_text_begin = font.render("Begin", True, button_text_color)

button_rect_salon = pygame.Rect(100, 400, 100, 100)
button_rect_saloon = pygame.Rect(500, 250, 100, 100)
button_rect_shop = pygame.Rect(700, 500, 100, 100)
button_rect_work = pygame.Rect(800, 375, 100, 100)
button_rect_bedroom = pygame.Rect(200, 240, 100, 100 )

button_rect_title = title_image.get_rect(center=(screen.get_width() // 2, 300))

coin_button_home = pygame.Rect(35, 600, 60, 60)
coin_button_else = pygame.Rect(35, 35, 60, 60)
button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

volume_on_img = pygame.transform.scale(volume_on_img, (60,60))
volume_off_img = pygame.transform.scale(volume_off_img, (60,60))
button_volume = pygame.Rect(930, 630, 60, 60)
volume_on = True

# --- Set music ---
pygame.mixer.music.load("data/audio/background_music.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0

screen_mode = "title"
running = True

while running:
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    if num_customers >= 20 and num_rows >= 50 and hydration >= 7:
        work_complete = True
    if num_aces >= 5 and num_spitballs >= 20 and num_beers >= 25:
        saloon_complete = True
    if num_dinners >=3 and num_desserts >=3 and num_twerks >= 50 and num_happiness >=30:
        salon_complete = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if screen_mode == "title":
                if button_rect_begin.collidepoint(mouse_pos):
                    screen_mode = "home"
            if screen_mode == "home":
                if button_rect_work.collidepoint(mouse_pos):
                    num_coins, num_customers, num_rows, hydration, happiness, volume_on, work_first_complete = run_work_game(num_coins, num_customers, num_rows, hydration, bow, gem, backpack, labubu, hat, heels, happiness,HAPPINESS_MAX, volume_on, work_first_open, work_first_complete)
                    if work_first_open:
                        work_first_open = False
                    current_world = "work"
                    if last_world != None:
                        connections.append([last_world, current_world])
                        miles_traveled += calculate_miles_traveled(current_world, last_world)
                        button_text_miles = button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True, button_color)
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    last_world = current_world
                if work_complete:
                    if button_rect_salon.collidepoint(mouse_pos):
                        num_coins, num_dinners, num_desserts, num_twerks, num_happiness, happiness, volume_on, salon_first_complete = run_salon_game(num_coins, num_dinners, num_desserts, num_twerks, num_happiness, happiness, bow, gem, backpack, hat, heels, labubu, HAPPINESS_MAX, volume_on, salon_first_open, salon_first_complete)
                        if salon_first_open:
                            salon_first_open = False
                        current_world = "salon"
                        if last_world != None:
                            connections.append([last_world, current_world])
                            miles_traveled += calculate_miles_traveled(current_world, last_world)
                            button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True,
                                                            button_color)
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                        last_world = current_world

                if salon_complete:
                    if button_rect_saloon.collidepoint(mouse_pos):
                        num_coins, num_aces, num_spitballs, num_beers, happiness, volume_on, saloon_first_complete = run_saloon_game(num_coins, num_aces, num_spitballs, num_beers, bow, gem, backpack, hat, heels, labubu, happiness, HAPPINESS_MAX, volume_on, saloon_first_open, saloon_first_complete)
                        if saloon_first_open:
                            saloon_first_open = False
                        current_world = "saloon"
                        if last_world != None:
                            connections.append([last_world, current_world])
                            miles_traveled += calculate_miles_traveled(current_world, last_world)
                            button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True,
                                                            button_color)
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                        last_world = current_world

                if saloon_complete:
                    if button_rect_bedroom.collidepoint(mouse_pos):
                        num_coins, web_coins, num_reads, happiness, volume_on, bedroom_first_complete = run_bedroom_game(num_coins, web_coins, num_reads, bow, gem, backpack, labubu, hat, heels, happiness, HAPPINESS_MAX, volume_on, bedroom_first_open, bedroom_first_complete)
                        if bedroom_first_open:
                            bedroom_first_open = False
                        current_world = "bedroom"
                        if last_world != None:
                            connections.append([last_world, current_world])
                            miles_traveled += calculate_miles_traveled(current_world, last_world)
                            button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True,
                                                            button_color)
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                        last_world = current_world

                if button_rect_shop.collidepoint(mouse_pos):
                    num_coins, happiness, bow, gem, backpack, hat, heels, labubu, volume_on = run_store(num_coins, happiness, bow, gem, backpack, hat, heels, labubu, HAPPINESS_MAX, volume_on)
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    current_world = "store"
                    if last_world != None:
                        connections.append([last_world, current_world])
                        miles_traveled += calculate_miles_traveled(current_world, last_world)
                        button_text_miles = font.render(f"Miles Traveled: {str(miles_traveled)}", True,
                                                        button_color)
                    last_world = current_world

                elif button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True

    # --- Drawing ---
    if screen_mode == "title":
        screen.blit(background, (0, 0))

        screen.blit(title_image, button_rect_title)

        pygame.draw.rect(screen, button_color, button_rect_begin, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect_begin, width=2, border_radius=10)
        screen.blit(button_text_begin, (button_rect_begin.x + 60, button_rect_begin.y + 5))

    elif screen_mode == "home":
        screen.blit(background, (0,0))

        for conn in connections:
            start_pos, end_pos = conn
            draw_dotted_line(screen, (0, 0, 0), start_pos, end_pos)

        screen.blit(pin, button_rect_work)

        screen.blit(pin, button_rect_salon)
        if not work_complete:
            screen.blit(lock, (button_rect_salon.x+20, button_rect_salon.y))

        screen.blit(pin, button_rect_saloon)
        if not salon_complete:
            screen.blit(lock, (button_rect_saloon.x+20, button_rect_saloon.y))

        screen.blit(pin, button_rect_bedroom)
        if not saloon_complete:
            screen.blit(lock, (button_rect_bedroom.x+20, button_rect_bedroom.y+20))
        screen.blit(pin, button_rect_shop)

        screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
        screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))

        # Tooltip list
        pin_tooltips = [
            (button_rect_salon, "Go to the Salon"),
            (button_rect_saloon, "Go to the Saloon"),
            (button_rect_shop, "Go to Shop"),
            (button_rect_work, "Go to Work"),
            (button_rect_bedroom, "Go Home"),
        ]

        draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

        for rect, tooltip in pin_tooltips:
            if rect.collidepoint(mouse_pos):
                tooltip_surf = font.render(tooltip, True, button_text_color)
                tooltip_bg_rect = pygame.Rect(
                    0, 0,
                    tooltip_surf.get_width() + 10,
                    tooltip_surf.get_height() + 6
                )
                tooltip_bg_rect.centerx = rect.centerx
                tooltip_bg_rect.bottom = rect.top - 5  # slightly above the pin
                pygame.draw.rect(screen, button_color, tooltip_bg_rect, border_radius=8)
                screen.blit(tooltip_surf, (tooltip_bg_rect.x + 5, tooltip_bg_rect.y + 3))

        screen.blit(button_text_miles, (button_rect_miles.x, button_rect_miles.y))
        screen.blit(button_text_carbon, (button_rect_carbon.x, button_rect_carbon.y))
        draw_face(miles_traveled, face_rect)

    pygame.display.flip()
    clock.tick(60)