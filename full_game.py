import pygame
import math
import json
import os
import copy
from pathlib import Path
import sys

from saloon import run_saloon_game
from salon import run_salon_game
from work import run_work_game
from bedroom import run_bedroom_game
from happiness import draw_happiness_meter
from store import run_store
from displays import announcement

app_name = "Prumpi_World"
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
        face = pygame.image.load(f"data/image/face0.png")
    elif 1000 <= miles_traveled < 10000:
        face = pygame.image.load(f"data/image/face1.png")
    elif 10000 <= miles_traveled < 20000:
        face = pygame.image.load(f"data/image/face2.png")
    elif 20000 <= miles_traveled < 30000:
        face = pygame.image.load(f"data/image/face3.png")
    elif 30000 <= miles_traveled < 40000:
        face = pygame.image.load(f"data/image/face4.png")
    elif 40000 <= miles_traveled:
        face = pygame.image.load(f"data/image/face5.png")
    face = pygame.transform.scale(face, (50, 50))
    screen.blit(face, face_rect)

def get_save_path():
    if sys.platform == "darwin":  # macOS
        base = Path.home() / "Library" / "Application Support" / app_name
    elif sys.platform == "win32":  # Windows
        base = Path(os.getenv("APPDATA")) / app_name
    else:  # Linux and others
        base = Path.home() / f".{app_name}"

    base.mkdir(parents=True, exist_ok=True)
    return base / "savegame.json"

def save_game():
    save_file = get_save_path()
    print(save_file)
    with open(save_file, "w") as f:
        json.dump(game_state, f)
    print("Saved!")

def load_game():
    global game_state
    save_file = get_save_path()
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            game_state = json.load(f)
        print("Loaded:", game_state)
    else:
        print("No save file found, starting fresh.")
        reset_game(save=False)

def reset_game(save=True):
    global game_state
    game_state = copy.deepcopy(default_state)
    if save:
        save_game()
    print("Game reset!")

# --- Initialize Game ---
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Prumpi World")
clock = pygame.time.Clock()

# --- Save Game ---
save_file = "savegame.json"

# GAME STATE VARIABLES
default_state = {
    "num_coins": 0,

    "game_first_open": True,

    # Accessories
    "bow": False,
    "gem": False,
    "backpack": False,
    "hat": False,
    "heels": False,
    "labubu": False,

    # Work
    "work_complete": False,
    "work_first_open": True,
    "work_first_complete": True,
    "num_customers": 0,
    "num_rows": 0,
    "hydration": 0,

    # Salon
    "salon_complete": False,
    "salon_first_open": True,
    "salon_first_complete": True,
    "num_dinners": 0,
    "num_desserts": 0,
    "num_twerks": 0,
    "num_happiness": 0,

    # Saloon
    "saloon_complete": False,
    "saloon_first_open": True,
    "saloon_first_complete": True,
    "num_aces": 0,
    "num_spitballs": 0,
    "num_beers": 0,

    # Bedroom
    "bedroom_complete": False,
    "bedroom_first_open": True,
    "bedroom_first_complete": True,
    "web_coins": 0,
    "num_reads": 0,

    # Happiness
    "happiness": 0,

    # Carbon footprint
    "miles_traveled": 0,
    "connections": [],
    "current_world": None,
    "last_world": None
}

game_state = copy.deepcopy(default_state)

# --- Set Font and Button Colors  ---
font = pygame.font.SysFont("comic_sansms", 32)
button_color = (255, 225, 125)
button_text_color = (24, 100, 24)

# --- Load images ---
background = pygame.image.load("data/image/prumpi_world.png")
title_image = pygame.image.load('data/image/world_title.png')
pin = pygame.image.load('data/image/pin.png')
volume_on_img = pygame.image.load("data/image/volume_on.png")
volume_off_img = pygame.image.load("data/image/volume_off.png")
coin_img = pygame.image.load("data/image/coin.png")
lock = pygame.image.load("data/image/lock.png")
arrow = pygame.image.load("data/image/arrow_yellow.png")

# --- Rescale images ---
background = pygame.transform.scale(background, (1000, 700))
title_image = pygame.transform.scale(title_image, (500, 300))
pin = pygame.transform.scale(pin, (100,100))
coin_img = pygame.transform.scale(coin_img, (80, 80))
lock = pygame.transform.scale(lock, (50,50))
volume_on_img = pygame.transform.scale(volume_on_img, (60,60))
volume_off_img = pygame.transform.scale(volume_off_img, (60,60))
arrow = pygame.transform.scale(arrow, (100,100))
arrow = pygame.transform.rotate(arrow, 90)

# --- Button Rects and Text
button_rect_miles = pygame.Rect(600, 20, 200, 60)

button_rect_carbon = pygame.Rect(600, 70, 200, 60)
button_text_carbon = font.render(f"Carbon Footprint:", True, button_color)

face_rect = pygame.Rect(875, 70, 50, 50)

button_rect_save = pygame.Rect(25, 20, 200, 50)
button_text_save = font.render(f"Save Game", True, button_text_color)

button_rect_new =  pygame.Rect(25, 90, 200, 50)
button_text_new = font.render(f"New Game", True, button_text_color)

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

button_rect_sure = pygame.Rect(250, 200, 500, 250)
button_text_sure_1 = font.render("Are you sure you", True, button_text_color)
button_text_sure_2 = font.render("want to start a new game?", True, button_text_color)

button_rect_yes = pygame.Rect(425, 380, 50, 50)
button_rect_no = pygame.Rect(525, 380, 50, 50)

button_volume = pygame.Rect(930, 630, 60, 60)

arrow_pos = (225, 85)

# --- Game variables not in JSON ---
volume_on = True
HAPPINESS_MAX = 30

are_you_sure = False
saving = False

page_1 = True
page_2 = False


# --- Set music ---
pygame.mixer.music.load("data/audio/background_music.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0

# --- Load game or start new save ---
load_game()

# --- Final variable settings ---
screen_mode = "title"
button_text_miles = font.render(f"Miles Traveled: " + str(game_state["miles_traveled"]), True,
                                                        button_color)
button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))

# --- Run game ---
running = True
while running:
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    if game_state["num_customers"] >= 20 and game_state["num_rows"] >= 50 and game_state["hydration"] >= 7:
        game_state["work_complete"] = True
    if game_state["num_aces"] >= 5 and game_state["num_spitballs"] >= 20 and game_state["num_beers"] >= 25:
        game_state["saloon_complete"] = True
    if game_state["num_dinners"] >=3 and game_state["num_dessert"] >=3 and game_state["num_twerks"] >= 50 and game_state["num_happiness"] >=30:
        game_state["salon_complete"] = True
    if game_state["num_reads"] >=5 and game_state["web_coins"] >=50:
        game_state["bedroom_complete"] = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if screen_mode == "title":
                if button_rect_begin.collidepoint(mouse_pos):
                    if game_state["game_first_open"]:
                        screen_mode = "instructions 1"
                    else:
                        screen_mode = "home"

            if screen_mode == "home":
                if button_rect_save.collidepoint(mouse_pos):
                    save_time = pygame.time.get_ticks()
                    saving = True
                    save_game()

                if button_rect_new.collidepoint(mouse_pos):
                    are_you_sure = True

                if are_you_sure:
                    if button_rect_yes.collidepoint(mouse_pos):
                        reset_game()
                        button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                        button_text_miles = font.render(f"Miles Traveled: " + str(game_state["miles_traveled"]), True,
                                                        button_color)
                        click_time = pygame.time.get_ticks()
                        are_you_sure = False
                    elif button_rect_no.collidepoint(mouse_pos):
                        are_you_sure = False

                if button_rect_work.collidepoint(mouse_pos):
                    game_state["num_coins"],game_state["num_customers"],game_state["num_rows"],game_state["hydration"],game_state["happiness"],volume_on,game_state["work_first_complete"] = run_work_game(
                        game_state["num_coins"],game_state["num_customers"],game_state["num_rows"],
                        game_state["hydration"],game_state["bow"],game_state["gem"],game_state["backpack"],
                        game_state["labubu"],game_state["hat"],game_state["heels"],game_state["happiness"],
                        HAPPINESS_MAX,volume_on,game_state["work_first_open"],game_state["work_first_complete"]
                    )
                    if game_state["work_first_open"]:
                        game_state["work_first_open"] = False
                    game_state["current_world"] = "work"
                    if  game_state["last_world"] is not None:
                        game_state["connections"].append([game_state["last_world"], game_state["current_world"]])
                        game_state["miles_traveled"] += calculate_miles_traveled(game_state["current_world"], game_state["last_world"])
                        button_text_miles = font.render(f"Miles Traveled: {str(game_state['miles_traveled'])}",
                                                        True, button_color)
                    button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                    game_state["last_world"] = game_state["current_world"]

                if game_state["work_complete"]:
                    if button_rect_salon.collidepoint(mouse_pos):
                        game_state["num_coins"],game_state["num_dinners"],game_state["num_desserts"],game_state["num_twerks"],game_state["num_happiness"],game_state["happiness"],volume_on,game_state["salon_first_complete"] = run_salon_game(
                            game_state["num_coins"],game_state["num_dinners"],game_state["num_desserts"],
                            game_state["num_twerks"],game_state["num_happiness"],game_state["happiness"],
                            game_state["bow"],game_state["gem"],game_state["backpack"],game_state["hat"],
                            game_state["heels"],game_state["labubu"],HAPPINESS_MAX,volume_on,
                            game_state["salon_first_open"],game_state["salon_first_complete"]
                        )
                        if game_state["salon_first_open"]:
                            game_state["salon_first_open"] = False
                        game_state["current_world"] = "salon"
                        if game_state["last_world"] is not None:
                            game_state["connections"].append([game_state["last_world"], game_state["current_world"]])
                            game_state["miles_traveled"] += calculate_miles_traveled(game_state["current_world"],
                                                                                     game_state["last_world"])
                            button_text_miles = font.render(f"Miles Traveled: {str(game_state['miles_traveled'])}",
                                                            True, button_color)
                        button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                        game_state["last_world"] = game_state["current_world"]

                if game_state["salon_complete"]:
                    if button_rect_saloon.collidepoint(mouse_pos):
                        game_state["num_coins"],game_state["num_aces"],game_state["num_spitballs"],game_state["num_beers"],game_state["happiness"],volume_on,game_state["saloon_first_complete"] = run_saloon_game(
                            game_state["num_coins"],game_state["num_aces"],game_state["num_spitballs"],
                            game_state["num_beers"],game_state["bow"],game_state["gem"],
                            game_state["backpack"],game_state["hat"],game_state["heels"],game_state["labubu"],
                            game_state["happiness"],HAPPINESS_MAX,volume_on,game_state["saloon_first_open"],game_state["saloon_first_complete"]
                        )
                        if game_state["saloon_first_open"]:
                            game_state["saloon_first_open"] = False
                        game_state["current_world"] = "saloon"
                        if game_state["last_world"] is not None:
                            game_state["connections"].append([game_state["last_world"], game_state["current_world"]])
                            game_state["miles_traveled"] += calculate_miles_traveled(game_state["current_world"],
                                                                                     game_state["last_world"])
                            button_text_miles = font.render(f"Miles Traveled: {str(game_state['miles_traveled'])}",
                                                            True, button_color)
                        button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                        game_state["last_world"] = game_state["current_world"]

                if game_state["saloon_complete"]:
                    if button_rect_bedroom.collidepoint(mouse_pos):
                        game_state["num_coins"],game_state["web_coins"],game_state["num_reads"],game_state["happiness"],volume_on,game_state["bedroom_first_complete"] = run_bedroom_game(
                            game_state["num_coins"],game_state["web_coins"],game_state["num_reads"],
                            game_state["bow"],game_state["gem"],game_state["backpack"],
                            game_state["labubu"],game_state["hat"],game_state["heels"],game_state["happiness"],
                            HAPPINESS_MAX,volume_on,game_state["bedroom_first_open"],game_state["bedroom_first_complete"]
                        )
                        if game_state["bedroom_first_open"]:
                            game_state["bedroom_first_open"] = False
                        game_state["current_world"] = "bedroom"
                        if game_state["last_world"] is not None:
                            game_state["connections"].append([game_state["last_world"], game_state["current_world"]])
                            game_state["miles_traveled"] += calculate_miles_traveled(game_state["current_world"],
                                                                                     game_state["last_world"])
                            button_text_miles = font.render(f"Miles Traveled: {str(game_state['miles_traveled'])}",
                                                            True, button_color)
                        button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                        game_state["last_world"] = game_state["current_world"]

                if button_rect_shop.collidepoint(mouse_pos):
                    (game_state["num_coins"],game_state["happiness"],game_state["bow"],game_state["gem"],game_state["backpack"],
                     game_state["hat"],game_state["heels"],game_state["labubu"],volume_on) = run_store(
                        game_state["num_coins"],game_state["happiness"],game_state["bow"],game_state["gem"],
                        game_state["backpack"],game_state["hat"],game_state["heels"],game_state["labubu"],
                        HAPPINESS_MAX,volume_on
                    )
                    button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                    game_state["current_world"] = "store"
                    if game_state["last_world"] is not None:
                        game_state["connections"].append([game_state["last_world"], game_state["current_world"]])
                        game_state["miles_traveled"] += calculate_miles_traveled(game_state["current_world"],
                                                                                 game_state["last_world"])
                        button_text_miles = font.render(f"Miles Traveled: {str(game_state['miles_traveled'])}",
                                                        True, button_color)
                    button_text_coin = font.render(str(game_state["num_coins"]) + " Prumpi Coins", True, (0, 0, 0))
                    game_state["last_world"] = game_state["current_world"]

            if button_volume.collidepoint(mouse_pos):
                if volume_on == True:
                    pygame.mixer.music.set_volume(0)
                    volume_on = False
                elif volume_on == False:
                    pygame.mixer.music.set_volume(0.5)
                    volume_on = True

        elif event.type == pygame.KEYDOWN:
            if screen_mode == "instructions 1":
                screen_mode = "instructions 2"
            elif screen_mode == "instructions 2":
                click_time = pygame.time.get_ticks()
                screen_mode = "home"

    # --- Drawing ---
    if screen_mode == "title":
        screen.blit(background, (0, 0))

        screen.blit(title_image, button_rect_title)

        pygame.draw.rect(screen, button_color, button_rect_begin, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect_begin, width=2, border_radius=10)
        screen.blit(button_text_begin, (button_rect_begin.x + 60, button_rect_begin.y + 5))

    elif screen_mode == "instructions 1":
        welcome_text_1 = "Hi I'm Prumpi! Welcome"
        welcome_text_2 = "to a day in my life! "
        welcome_text_3 = "Press any key to continue."
        announcement(screen, background, welcome_text_1, welcome_text_2, welcome_text_3)
    elif screen_mode == "instructions 2":
        welcome_text_1 = "Complete quests to unlock"
        welcome_text_2 = "new places. Let's go to work!"
        welcome_text_3 = "Press any key to continue."
        announcement(screen, background, welcome_text_1, welcome_text_2, welcome_text_3)

    elif screen_mode == "home":
        screen.blit(background, (0,0))

        pygame.draw.rect(screen, button_color, button_rect_save, border_radius=10)
        screen.blit(button_text_save, button_rect_save)
        pygame.draw.rect(screen, button_color, button_rect_new, border_radius=10)
        screen.blit(button_text_new, button_rect_new)


        for conn in game_state["connections"]:
            start_pos, end_pos = conn
            draw_dotted_line(screen, (0, 0, 0), start_pos, end_pos)

        screen.blit(pin, button_rect_work)

        screen.blit(pin, button_rect_salon)
        if not game_state["work_complete"]:
            screen.blit(lock, (button_rect_salon.x+20, button_rect_salon.y))

        screen.blit(pin, button_rect_saloon)
        if not game_state["salon_complete"]:
            screen.blit(lock, (button_rect_saloon.x+20, button_rect_saloon.y))

        screen.blit(pin, button_rect_bedroom)
        if not game_state["saloon_complete"]:
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

        draw_happiness_meter(screen, game_state["happiness"], HAPPINESS_MAX)

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
        draw_face(game_state["miles_traveled"], face_rect)

        if are_you_sure:
            pygame.draw.rect(screen, button_color, button_rect_sure, border_radius=10)
            screen.blit(button_text_sure_1, (button_rect_sure.x, button_rect_sure.y+25))
            screen.blit(button_text_sure_2, (button_rect_sure.x, button_rect_sure.y + 50))
            pygame.draw.rect(screen, (150, 255, 150), button_rect_yes, border_radius=10)
            screen.blit(font.render("Yes", True, (0,0,0,)), (button_rect_yes[0], button_rect_yes[1]))
            pygame.draw.rect(screen, (255, 150, 150), button_rect_no, border_radius=10)
            screen.blit(font.render("No", True, (0,0,0,)), (button_rect_no[0], button_rect_no[1]))

        if saving and pygame.time.get_ticks() - save_time < 2000:
            screen.blit(font.render("Saving!!!", True, button_color), (250, 20))

        if game_state["game_first_open"] and pygame.time.get_ticks() - click_time < 5000:
            screen.blit(arrow, arrow_pos)
            instructions_1 = font.render("Save or start a new game", True, button_color)
            instructions_2 = font.render("on the home page!", True, button_color)
            screen.blit(instructions_1, (arrow_pos[0], arrow_pos[1] + 90))
            screen.blit(instructions_2, (arrow_pos[0], arrow_pos[1] + 120))
        else:
            game_state["game_first_open"] = False



    pygame.display.flip()
    clock.tick(60)