
import pygame
import sys
import random
from collections import deque
from minigame import twerk_minigame_menu


# Currency stuff
num_coins = 100

# Functions
def generate_dirt_splotches(num_splotches=20):
    '''
    Generates dirt splotches to go on Prumpi's scales

    :param num_splotches: number of dirt splotches on Prumpi's scales
    :return: coordinates of the splotches
    '''
    splotches = []
    for _ in range(num_splotches):
        x = random.randint(200, 800)  # adjust these to fit your scales area
        y = random.randint(200, 600)
        radius = random.randint(50, 100)
        splotches.append({"pos": (x, y), "radius": radius})
    return splotches

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

def colors_equal(c1, c2):
    return c1[:3] == c2[:3]  # compare RGB only, ignore alpha

def flood_fill(surface, x, y, fill_color):
    '''
    flood fills Prumpi's nails
    :param surface: background screen
    :param x: click coordinate
    :param y: click coordinate
    :param fill_color: color selected from color bar for the nail to be filled with
    '''
    target_color = surface.get_at((x, y))
    if colors_equal(target_color, fill_color):
        return

    w, h = surface.get_size()
    q = deque()
    q.append((x, y))

    while q:
        cx, cy = q.popleft()
        if 0 <= cx < w and 0 <= cy < h:
            current_color = surface.get_at((cx, cy))
            if colors_equal(current_color, target_color):
                surface.set_at((cx, cy), fill_color)
                q.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])


# --- Initialize Game ---
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Dino Beauty Salon")
clock = pygame.time.Clock()

# --- Sets the default state to the home screen---
screen_mode = "home"

# --- Load images ---
title_image = pygame.image.load("data/image/title.png").convert_alpha()
background = pygame.image.load("data/image/salon.png")
dino = pygame.image.load("data/image/prumpi.png")
nails_screen = pygame.image.load("data/image/nails.png")
dino_eating = pygame.image.load("data/image/open_mouth.png")
dino_closed_mouth = pygame.image.load("data/image/closed_mouth.png")  # Add your closed mouth image
fish_img = pygame.image.load("data/image/fish.png")
reset_img = pygame.image.load("data/image/reset_icon.png").convert_alpha()
chocolate_img = pygame.image.load("data/image/chocolate.png").convert_alpha()
scales_bg = pygame.image.load("data/image/scales.png")
dirt_texture = pygame.image.load("data/image/dirt_texture.png").convert_alpha()
broom_img = pygame.image.load("data/image/broom.png").convert_alpha()
curtain_img = pygame.image.load("data/image/curtain.png").convert_alpha()
alley_screen = pygame.image.load("data/image/alley.png")
volume_on_img = pygame.image.load("data/image/volume_on.png")
volume_off_img = pygame.image.load("data/image/volume_off.png")
coin_img = pygame.image.load("data/image/coin.png")
shop_screen = pygame.image.load("data/image/shop.png")
bow_img = pygame.image.load("data/image/bow.png")
check = pygame.image.load("data/image/check.png")
gem_img = pygame.image.load("data/image/gem.png")
backpack_img = pygame.image.load("data/image/backpack.png")
prumpi_backpack = pygame.image.load("data/image/prumpi_backpack.png")


# --- Resize images ---
title_image = pygame.transform.scale(title_image, (500,300))
background = pygame.transform.scale(background, (1000, 700))
alley_screen = pygame.transform.scale(alley_screen, (1000, 700))
scales_bg = pygame.transform.scale(scales_bg, (1000, 700))
dino = pygame.transform.scale(dino, (300, 400))
prumpi_backpack = pygame.transform.scale(prumpi_backpack, (300, 400))
nails_screen = pygame.transform.scale(nails_screen, (1000, 700))
original_nails_screen = nails_screen.copy()
dino_eating = pygame.transform.scale(dino_eating, (1000, 700))
dino_closed_mouth = pygame.transform.scale(dino_closed_mouth, (1000, 700))
fish_img = pygame.transform.scale(fish_img, (80, 80)) #USED TO BE 40
chocolate_img = pygame.transform.scale(chocolate_img, (80, 80))  # used to be same size as fish_img
broom_img = pygame.transform.scale(broom_img, (120, 120))  # adjust size as needed
curtain_img = pygame.transform.scale(curtain_img, (1000, 700))  # Adjust to your screen size
coin_img = pygame.transform.scale(coin_img, (80,80))
shop_screen = pygame.transform.scale(shop_screen, (1000,700))
check = pygame.transform.scale(check, (50,50))

# --- Set Font and Button Colors  ---
font = pygame.font.SysFont("comic_sansms", 32)
button_color = (255, 225, 125)
button_text_color = (24, 100, 24)

# --- Create buttons ---
button_text_begin = font.render("Begin", True, button_text_color)

# Home screen
button_rect_home_paint = pygame.Rect(750, 20, 200, 60)
button_text_paint = font.render("Paint Nails", True, button_text_color)

button_rect_home_dinner = pygame.Rect(750, 90, 200, 60)
button_text_dinner = font.render("Dinner Time", True, button_text_color)

button_rect_home_grooming = pygame.Rect(750, 160, 200, 60)
button_text_grooming = font.render("Grooming", True, button_text_color)

button_rect_home_dance = pygame.Rect(750, 230, 200, 60)
button_text_dance = font.render("Dance Time", True, button_text_color)

button_rect_alley = pygame.Rect(50,20,100,50)
button_text_alley = font.render('Break', True, button_text_color)

button_rect_shop = pygame.Rect(50,90,100,50)
button_text_shop = font.render('Shop', True, button_text_color)

# All screens
button_rect_home = pygame.Rect(700, 30, 250, 60)
button_text_home = font.render("Return Home", True, button_text_color)

reset_img = pygame.transform.scale(reset_img, (60, 60))
button_reset = pygame.Rect(930, 530, 60, 60)

volume_on_img = pygame.transform.scale(volume_on_img, (60,60))
volume_off_img = pygame.transform.scale(volume_off_img, (60,60))
button_volume = pygame.Rect(930, 630, 60, 60)
volume_on = True

# Dinner
button_hardfiskur = pygame.Rect(25, 150, 200, 60)
button_kokosbollar = pygame.Rect(25, 230, 200, 60)
button_text_hardfiskur = font.render("Harðfiskur", True, button_text_color)
button_text_kokosbollar = font.render("Kokosbollar", True, button_text_color)

# Alley
button_rect_be_naughty = pygame.Rect(675, 550, 300, 60)
button_text_be_naughty = font.render("Be naughty... (15¢)", True, button_text_color)
shrink_button_rect = pygame.Rect(30, 630, 140, 50)


coin_button_home = pygame.Rect(35, 600, 60, 60)
coin_button_else = pygame.Rect(35,35,60,60)
button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0,0,0))

# --- Specific Screen Parameters ---
#Opening Screen stuff
screen_mode = "title"
curtain_y = 0  # Start fully covering screen
curtain_opening = False
curtain_speed = 10

# Main salon
dino_pos = (315, 125)
stomach_hitbox = pygame.Rect(350, 225, 200, 200)
mouse_in_stomach = False
tickle_start_time = None
giggle_triggered = False
GIGGLE_DURATION = 2  # seconds the speech bubble stays
giggle_start_time = None

# Alley transition
exit_sound = pygame.mixer.Sound("data/audio/exit_sequence.mp3")
transition_start_time = None
exit_sound_playing = False

# Alley
dino_pos_alley = (315, 250)
cylinder_max_width = 250 #used to be 300
cylinder_height = 40
cylinder_width = cylinder_max_width
cylinder_orig_pos = (110,450)
cylinder_pos = cylinder_orig_pos
shrinking = False
shrink_start_time = None
total_shrink_time = 0  # accumulate total time held
show_fiend = False
fiend_start_time = 0
fiend_duration = 3000  # milliseconds (3 seconds)
cigarette = False

smoke_frames = []
for i in range(2):  # change if you have more or fewer frames
    img = pygame.image.load(f"data/image/smoke_{i+1}.png").convert_alpha()
    img = pygame.transform.scale(img, (50, 50))  # resize as needed
    smoke_frames.append(img)
smoke_frame_index = 0
smoke_frame_timer = 0
smoke_frame_interval = 100  # milliseconds per frame


# Nails
nail_areas = [pygame.Rect(x-25, y-25, 50, 50) for x, y in [
    (850, 66), (115, 488), (212, 523), (330, 540),
    (450, 480), (550, 475), (675, 540), (790, 530), (880, 480)
]]
nail_colors = [None for _ in nail_areas]
color_options = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 105, 180), # Hot Pink
    (160, 32, 240),  # Purple
]
color_buttons = []
selected_color_index = 0
paint_color = color_options[selected_color_index]  # initial color
# Generate rects for nail color buttons (bottom left corner)
for i in range(len(color_options)):
    x = 20 + i * 50  # spacing
    y = 640
    color_buttons.append(pygame.Rect(x, y, 40, 40))
nail_thank_you = False

# Dinner
initial_fish_positions = [(50 + i * 90, 600) for i in range(5)]
fish_rects = [pygame.Rect(x, y, 80, 80) for x, y in initial_fish_positions]

dragging_fish = None
mouse_offset = (0, 0)
mouth_rect = pygame.Rect(250, 300, 400, 250)  # approx dino mouth

active_food = "fish"

chewing = False
chewing_start_time = 0
chewing_duration = 250  # milliseconds

show_thank_you = False
thank_you_start_time = 0
thank_you_duration = 2000  # milliseconds

# Grooming
dirt_splotches = generate_dirt_splotches()
erasing = False

broom_rect = broom_img.get_rect(topleft=(20, 300))

dragging_broom = False
mouse_offset = (0, 0)

show_clean_message = False
clean_message_start_time = 0
clean_message_duration = 2000  #ms

# Shop
bow = False
item_1_rect = pygame.Rect(200, 125, 100, 100)
item_1_text = font.render('30¢', True, button_text_color)

gem = False
item_2_rect = pygame.Rect(400, 125, 100, 100)
item_2_text = font.render('50¢', True, button_text_color)

backpack = False
item_3_rect = pygame.Rect(600, 125, 100, 100)
item_3_text = font.render('100¢', True, button_text_color)


# Music
pygame.mixer.music.load("data/audio/background_music.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0


# Game loop
running = True
while running:
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if screen_mode not in ["title", "alley_transition"]:
                if button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True

            # Navigates to different modes upon clicking buttons from home screen
            if screen_mode == "home":
                if button_rect_home_paint.collidepoint(mouse_pos):
                    screen_mode = "nails"
                elif button_rect_home_dinner.collidepoint(mouse_pos):
                    screen_mode = "dinner"
                elif button_rect_home_grooming.collidepoint(mouse_pos):
                    screen_mode = "grooming"
                elif button_rect_alley.collidepoint(mouse_pos):
                    # pygame.mixer.music.pause()
                    pygame.mixer.music.fadeout(1000)
                    fade_to_black(screen, clock, background, speed=5)
                    screen_mode = "alley_transition"
                    exit_sound.play()
                    exit_sound_playing = True
                elif button_rect_shop.collidepoint(mouse_pos):
                    screen_mode = "shop"
                elif button_rect_home_dance.collidepoint(mouse_pos):
                    screen_mode = "dance"

            elif screen_mode == "title":
                if button_rect.collidepoint(event.pos):
                    curtain_opening = True

            elif screen_mode == "alley":
                if button_rect_home.collidepoint(mouse_pos):
                    pygame.mixer.music.fadeout(10)
                    screen_mode = "home"
                    pygame.mixer.music.load("data/audio/background_music.mp3")
                    pygame.mixer.music.play(-1)
                if shrink_button_rect.collidepoint(mouse_pos) and cigarette:
                    if not shrinking:
                        shrinking = True
                        shrink_start_time = pygame.time.get_ticks()
                if button_rect_be_naughty.collidepoint(mouse_pos):
                    if num_coins >= 15:
                        cigarette=True
                        total_shrink_time = 0
                        shrink_start_time = None
                        shrinking = False
                        cylinder_width = cylinder_max_width
                        cylinder_pos = cylinder_orig_pos
                        show_fiend = False  # Also hide "another one" bubble if shown
                        fiend_start_time = None
                        num_coins -= 15
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    else:
                        #Print that you need more coins for that...
                        None

            elif screen_mode == "nails":
                # Sets different click functions in the nail screen
                # # Navigates to the home screen
                if button_rect_home.collidepoint(mouse_pos):
                    screen_mode = "home"
                    nail_colors = [None for _ in nail_colors]
                    nails_screen = original_nails_screen.copy()
                else:
                    for i, nail_rect in enumerate(nail_areas):
                        if nail_rect.collidepoint(mouse_pos):
                            seed_x, seed_y = nail_rect.center
                            flood_fill(nails_screen, seed_x, seed_y, paint_color)

                            if nail_colors[i] is None:
                                nail_colors[i] = paint_color
                                # print(nail_colors)
                                if not nail_thank_you and all(c is not None for c in nail_colors[1:]):
                                    nail_thank_you = True
                                    num_coins += 5
                                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                                    thank_you_start_time = pygame.time.get_ticks()
                            else:
                                nail_colors[i]=paint_color
                        # Check if any color button was clicked
                        for i, rect in enumerate(color_buttons):
                            if rect.collidepoint(mouse_pos):
                                selected_color_index = i
                                paint_color = color_options[i]
                # Check reset button
                if button_reset.collidepoint(mouse_pos):
                    nail_colors = [None for _ in nail_colors]
                    nails_screen = original_nails_screen.copy()
                    screen.blit(nails_screen, (0, 0))

            elif screen_mode == "dinner":
                #Sets the different click functions in the dinner screen
                # Navigates to the home screen
                if button_rect_home.collidepoint(mouse_pos):
                    screen_mode = "home"
                    fish_rects = [pygame.Rect(x, y, 80, 80) for x, y in initial_fish_positions]
                # Sets the food to fish when clicking the hardfiskur button
                if button_hardfiskur.collidepoint(mouse_pos):
                    active_food = "fish"
                    # reset fish positions when switching food type
                    fish_rects = [pygame.Rect(x, y, 80, 80) for x, y in initial_fish_positions]
                # Sets the food to kokosbollar when clicking the kokosbollar button
                elif button_kokosbollar.collidepoint(mouse_pos):
                    active_food = "chocolate"
                    # create candy positions same as fish positions (reusing the same layout)
                    fish_rects = [pygame.Rect(x, y, 80, 80) for x, y in initial_fish_positions]
                # Dragging fish
                for i, rect in enumerate(fish_rects):
                    if rect and rect.collidepoint(mouse_pos):
                        dragging_fish = i
                        mouse_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                # Resetting the screen button
                if button_reset.collidepoint(mouse_pos):
                    fish_rects = [pygame.Rect(x, y, 80, 80) for x, y in initial_fish_positions]

            elif screen_mode == "grooming":
                if button_rect_home.collidepoint(mouse_pos):
                    screen_mode = "home"
                    dirt_splotches = generate_dirt_splotches()
                    broom_rect = broom_img.get_rect(topleft=(20, 300))
                # erasing = True  # start erasing when mouse pressed down in grooming mode
                if broom_rect.collidepoint(event.pos):
                    erasing = True
                    dragging_broom = True
                    # Calculate offset so broom doesn't jump on drag start
                    mouse_offset = (mouse_pos[0] - broom_rect.x, event.pos[1] - broom_rect.y)
                if button_reset.collidepoint(mouse_pos):
                    dirt_splotches = generate_dirt_splotches()
                    broom_rect = broom_img.get_rect(topleft=(20, 300))

            elif screen_mode == "shop":
                if button_rect_home.collidepoint(mouse_pos):
                    screen_mode = "home"
                if item_1_rect.collidepoint(mouse_pos) and num_coins >= 30 and bow==False:
                    bow=True
                    num_coins-=30
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                if item_2_rect.collidepoint(mouse_pos) and num_coins >= 50 and gem==False:
                    gem=True
                    num_coins-=50
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                if item_3_rect.collidepoint(mouse_pos) and num_coins >= 100 and backpack==False:
                    backpack=True
                    num_coins-=100
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if screen_mode == "grooming":
                erasing = False  # stop erasing on mouse up
                dragging_broom = False

            elif screen_mode == "alley":
                if shrinking:
                    # Add how long it was held this time
                    time_held = pygame.time.get_ticks() - shrink_start_time
                    total_shrink_time += time_held
                    shrinking = False
                    shrink_start_time = None

            elif screen_mode == "dinner" and dragging_fish is not None:
                # Eats a fish and shows the chewing screen
                if mouth_rect.collidepoint(fish_rects[dragging_fish].center):
                    fish_rects[dragging_fish] = None  # "eaten"
                    chewing = True
                    chewing_start_time = pygame.time.get_ticks()
                dragging_fish = None
                # Check if all fish are eaten and say thank you if yes
                if all(f is None for f in fish_rects):
                    show_thank_you = True
                    num_coins += 5
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    thank_you_start_time = pygame.time.get_ticks()

        elif event.type == pygame.MOUSEMOTION:
            if screen_mode == "grooming" and erasing == True:
                broom_rect.x = mouse_pos[0] - mouse_offset[0]
                broom_rect.y = mouse_pos[1] - mouse_offset[1]
                # Remove any dirt splotch under the mouse pointer
                dirt_splotches = [
                    d for d in dirt_splotches
                    if (mouse_pos[0] - d["pos"][0]) ** 2 + (mouse_pos[1] - d["pos"][1]) ** 2 > d["radius"] ** 2
                ]
                if screen_mode == "grooming" and len(dirt_splotches) == 0 and not show_clean_message:
                    num_coins += 5
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    show_clean_message = True
                    clean_message_start_time = pygame.time.get_ticks()

            elif screen_mode == "dinner" and dragging_fish is not None and fish_rects[dragging_fish]:
                fish_rects[dragging_fish].x = mouse_pos[0] - mouse_offset[0]
                fish_rects[dragging_fish].y = mouse_pos[1] - mouse_offset[1]

            elif screen_mode == "home":
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:  # Left mouse button is held
                    if stomach_hitbox.collidepoint(event.pos):
                        if tickle_start_time is None:
                            tickle_start_time = pygame.time.get_ticks()
                        else:
                            elapsed = (pygame.time.get_ticks() - tickle_start_time) / 1000
                            if elapsed >= 3 and not giggle_triggered:
                                giggle_triggered = True
                                giggle_start_time = pygame.time.get_ticks()
                    else:
                        # Left button is held but mouse left the hitbox → reset timer
                        tickle_start_time = None
                else:
                    # Left button is released → reset timer
                    tickle_start_time = None

            elif screen_mode == "grooming" and dragging_broom == True:
            # Move broom rect with mouse (keeping offset)
                broom_rect.x = event.pos[0] - mouse_offset[0]
                broom_rect.y = event.pos[1] - mouse_offset[1]
                # Erase dirt patches that broom touches
                broom_center = broom_rect.center
                dirt_splotches = [
                    d for d in dirt_splotches
                    if (broom_center[0] - d["pos"][0]) ** 2 + (broom_center[1] - d["pos"][1]) ** 2 > d["radius"] ** 2
                ]

    if screen_mode == "title" and curtain_opening:
        curtain_y -= curtain_speed
        if curtain_y + curtain_img.get_height() <= 0:
            screen_mode = "home"
            curtain_opening = False
    # --- Draw sections ---
    if screen_mode == "home":
        screen.blit(background, (0, 0))
        screen.blit(dino, dino_pos)
        pygame.draw.rect(screen, button_color, button_rect_home_paint, border_radius=12)
        screen.blit(button_text_paint, (button_rect_home_paint.x + 20, button_rect_home_paint.y + 10))
        pygame.draw.rect(screen, button_color, button_rect_home_dinner, border_radius=12)
        screen.blit(button_text_dinner, (button_rect_home_dinner.x + 10, button_rect_home_dinner.y + 10))
        pygame.draw.rect(screen, button_color, button_rect_home_grooming, border_radius=12)
        screen.blit(button_text_grooming, (button_rect_home_grooming.x + 30, button_rect_home_grooming.y + 10))
        pygame.draw.rect(screen, button_color, button_rect_alley, border_radius=12)
        screen.blit(button_text_alley, (button_rect_alley.x, button_rect_alley.y))
        pygame.draw.rect(screen, button_color, button_rect_shop, border_radius=12)
        screen.blit(button_text_shop, (button_rect_shop.x, button_rect_shop.y))
        pygame.draw.rect(screen, button_color, button_rect_home_dance, border_radius=12)
        screen.blit(button_text_dance, (button_rect_home_dance.x + 20, button_rect_home_dance.y + 10))
        if giggle_triggered:
            elapsed_since_giggle = (pygame.time.get_ticks() - giggle_start_time) / 1000
            if elapsed_since_giggle <= GIGGLE_DURATION:
                # Draw the "That tickles!" bubble
                bubble_rect = pygame.Rect(75, 200, 250, 80)
                pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=15)
                pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 2, border_radius=15)
                text = font.render("That tickles!", True, (0,0,0))
                screen.blit(text, (bubble_rect.x + 20, bubble_rect.y + 15))
            else:
                giggle_triggered = False  # reset after bubble disappears
        #put volume button
        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))
        if backpack:
            screen.blit(prumpi_backpack, dino_pos)
        if bow:
            bow_img =pygame.transform.scale(bow_img, (40,40))
            screen.blit(bow_img, (475, 175))
        if gem:
            gem_img = pygame.transform.scale(gem_img, (10,10))
            screen.blit(gem_img, (397,274))
        screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
        screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

    elif screen_mode == "title":
        # Draw background behind curtain (so it's already there as it pulls up)
        screen.blit(background, (0, 0))  # or use a solid color for stage
        screen.blit(curtain_img, (0, curtain_y))  # 2. Then draw the curtain
        # Title
        title_rect = title_image.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_image, title_rect)
        # Begin button
        button_rect = pygame.Rect(screen.get_width() // 2 - 100, 600, 200, 60)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, button_color, button_rect, width=2, border_radius=10)
        screen.blit(button_text_begin, (button_rect.x + 60, button_rect.y + 5))

    elif screen_mode == "alley_transition":
        screen.fill((0, 0, 0))  # black screen
        # Check if exit_sequence.mp3 is done
        if exit_sound_playing and not pygame.mixer.get_busy():
            # Sound finished, switch to alley
            screen_mode = "alley"
            exit_sound_playing = False

    elif screen_mode == "alley":
        if not pygame.mixer.music.get_busy() or current_music != "alley":
            pygame.mixer.music.load("data/audio/alley_music.mp3")
            pygame.mixer.music.play(-1)
            current_music = "alley"
        screen.blit(alley_screen, (0,0))
        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))
        screen.blit(dino, dino_pos_alley)
        if num_coins < 15:
            this_button_color =(180, 170, 140)
        else:
            this_button_color = button_color
        pygame.draw.rect(screen, this_button_color, button_rect_be_naughty, border_radius=12)
        screen.blit(button_text_be_naughty, (button_rect_be_naughty.x, button_rect_be_naughty.y))

        screen.blit(coin_img, (coin_button_else.x, coin_button_else.y))
        screen.blit(button_text_coin, (coin_button_else.x + 100, coin_button_else.y + 20))

        # Draw cylinder
        if cigarette or shrinking:
            draw_y = cylinder_pos[1]
            if shrinking:
                draw_y -= 60  # move up 100 pixels
            pygame.draw.rect(screen, (181, 101, 29), pygame.Rect(355, draw_y, 50, 40), border_radius=0)
            if cylinder_width > 0:
                cylinder_rect = pygame.Rect(
                    cylinder_pos[0] + (cylinder_max_width - cylinder_width),  # shift to the right as it shrinks
                    draw_y,
                    cylinder_width,
                    cylinder_height
                )
                pygame.draw.rect(screen, (180, 180, 200), cylinder_rect, border_radius=0)
                pygame.draw.rect(screen, (100, 100, 120), cylinder_rect, width=2, border_radius=0)
                # Draw smoke at right end while shrinking
                if shrinking:
                    smoke_img = smoke_frames[smoke_frame_index]
                    smoke_x = cylinder_rect.left - smoke_img.get_width() // 2
                    smoke_y = draw_y + 20 - smoke_img.get_height() // 2
                    screen.blit(smoke_img, (smoke_x, smoke_y))
            # Draw shrink button
            pygame.draw.rect(screen, button_color, shrink_button_rect, border_radius=10)
            shrink_text = font.render("Sesh", True, button_text_color)
            screen.blit(shrink_text, (shrink_button_rect.x + 30, shrink_button_rect.y))
        if show_fiend:
            # Bubble size and position
            bubble_width = 200
            bubble_height = 80
            bubble_x = cylinder_pos[0] + 50
            bubble_y = cylinder_pos[1] - 200  # above the cylinder
            bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
            # Draw bubble background
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), bubble_rect, width=2, border_radius=15)
            # Text
            speech_text = font.render("Another one!", True, (0, 0, 0))
            text_rect = speech_text.get_rect(center=bubble_rect.center)
            screen.blit(speech_text, text_rect)
        # put volume button
        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))
        if backpack:
            screen.blit(prumpi_backpack, dino_pos_alley)
        if bow:
            bow_img =pygame.transform.scale(bow_img, (40,40))
            screen.blit(bow_img, (475, 300))
        if gem:
            gem_img = pygame.transform.scale(gem_img, (10,10))
            screen.blit(gem_img, (397,399))

    elif screen_mode == "nails":
        screen.blit(nails_screen, (0, 0))
        # Show speech bubble if all fish eaten
        current_time = pygame.time.get_ticks()

        screen.blit(coin_img, (coin_button_else.x, coin_button_else.y))
        screen.blit(button_text_coin, (coin_button_else.x + 100, coin_button_else.y + 20))

        if nail_thank_you and (current_time - thank_you_start_time < thank_you_duration):
            # Bubble background
            bubble_rect = pygame.Rect(50, 150, 300, 80)
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bubble_rect, width=2, border_radius=10)
            # Speech text
            if all(c in ((255, 255, 0), (160, 32, 240)) for c in nail_colors[1:]):
                text = font.render("Go Lakers!", True, (0,0,0))
            else:
                text = font.render("I feel so pretty!", True, (0, 0, 0))
            screen.blit(text, (bubble_rect.x + 20, bubble_rect.y + 20))
        else:
            nail_thank_you = False

        #put volume button
        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))

        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))

        # Draw color buttons
        for i, rect in enumerate(color_buttons):
            pygame.draw.rect(screen, color_options[i], rect, border_radius=8)
            if i == selected_color_index:
                pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=8)  # Outline
        # Draw reset button
        screen.blit(reset_img, (button_reset.x, button_reset.y))

    elif screen_mode == "dinner":
        # Show chewing or open mouth depending on timer
        current_time = pygame.time.get_ticks()
        if chewing and (current_time - chewing_start_time < chewing_duration):
            screen.blit(dino_closed_mouth, (0, 0))
        else:
            screen.blit(dino_eating, (0, 0))
            chewing = False
        updated_fish_rects = []

        screen.blit(coin_img, (coin_button_else.x, coin_button_else.y))
        screen.blit(button_text_coin, (coin_button_else.x + 100, coin_button_else.y + 20))

        for rect in fish_rects:
            if rect is not None:
                if active_food == "fish":
                    screen.blit(fish_img, rect.topleft)
                else:  # chocolate
                    screen.blit(chocolate_img, rect.topleft)
                updated_fish_rects.append(rect)
        fish_rects = updated_fish_rects

        # Show speech bubble if all fish eaten
        current_time = pygame.time.get_ticks()
        if show_thank_you and (current_time - thank_you_start_time < thank_you_duration):
            # Bubble background
            bubble_rect = pygame.Rect(50, 300, 300, 80)
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bubble_rect, width=2, border_radius=10)
            # Speech text
            text = font.render("Thank you mamma!", True, (0, 0, 0))
            screen.blit(text, (bubble_rect.x + 20, bubble_rect.y + 20))
        else:
            show_thank_you = False

        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))
        screen.blit(reset_img, (button_reset.x, button_reset.y))

        pygame.draw.rect(screen, button_color, button_hardfiskur, border_radius=12)
        screen.blit(button_text_hardfiskur, (button_hardfiskur.x + 20, button_hardfiskur.y + 10))

        pygame.draw.rect(screen, button_color, button_kokosbollar, border_radius=12)
        screen.blit(button_text_kokosbollar, (button_kokosbollar.x + 20, button_kokosbollar.y + 10))

        #put volume button
        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))

    elif screen_mode == "grooming":
        screen.blit(scales_bg, (0, 0))

        screen.blit(coin_img, (coin_button_else.x, coin_button_else.y))
        screen.blit(button_text_coin, (coin_button_else.x + 100, coin_button_else.y + 20))

        # Draw dirt splotches
        for d in dirt_splotches:
            size = d["radius"] * 2
            texture_scaled = pygame.transform.smoothscale(dirt_texture, (size, size))
            # blit centered on pos
            pos = (d["pos"][0] - d["radius"], d["pos"][1] - d["radius"])
            screen.blit(texture_scaled, pos)
        if show_clean_message:
            current_time = pygame.time.get_ticks()
            if current_time - clean_message_start_time < clean_message_duration:
                # Draw speech bubble
                bubble_rect = pygame.Rect(200, 100, 300, 80)
                pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=12)
                pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 3, border_radius=12)
                text = font.render("All clean! Takk!", True, (0, 0, 0))
                screen.blit(text, (bubble_rect.x + 20, bubble_rect.y + 25))

            else:
                show_clean_message = False

        # Draw broom
        screen.blit(broom_img, broom_rect.topleft)

        # Draw back to home button (reuse your existing home button)
        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))
        screen.blit(reset_img, (button_reset.x, button_reset.y))

        #put volume button
        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))

    elif screen_mode == "shop":
        screen.blit(shop_screen, (0, 0))

        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))

        if volume_on == True:
            screen.blit(volume_on_img, (button_volume.x, button_volume.y))
        elif volume_on == False:
            screen.blit(volume_off_img, (button_volume.x, button_volume.y))

        bow_img = pygame.transform.scale(bow_img, (100,100))
        screen.blit(bow_img, (item_1_rect.x, item_1_rect.y))
        if bow==False:
            screen.blit(item_1_text, (item_1_rect.x + 20, item_1_rect.y+80))
        if bow==True:
            screen.blit(check, (item_1_rect.x+30, item_1_rect.y+30))

        gem_img = pygame.transform.scale(gem_img, (75, 75))
        screen.blit(gem_img, (item_2_rect.x + 12.5, item_2_rect.y+12.5))
        if gem==False:
            screen.blit(item_2_text, (item_2_rect.x + 20, item_2_rect.y+80))
        if gem==True:
            screen.blit(check, (item_2_rect.x+30, item_2_rect.y+30))

        backpack_img = pygame.transform.scale(backpack_img, (100, 100))
        screen.blit(backpack_img, (item_3_rect.x, item_3_rect.y))
        if backpack==False:
            screen.blit(item_3_text, (item_3_rect.x + 20, item_3_rect.y+80))
        if backpack==True:
            screen.blit(check, (item_3_rect.x+30, item_3_rect.y+30))

        screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
        screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

    elif screen_mode == "dance":
        coins, back_to_game = twerk_minigame_menu()
        num_coins += coins
        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
        if back_to_game:
            screen_mode = "home"  # or whatever you call your home screen

    # shrinking logic (move later)
    if screen_mode == "alley":
        # Compute total shrink duration (current hold + past holds)
        current_hold = 0
        if shrinking and cylinder_width >= 0:
            current_hold = pygame.time.get_ticks() - shrink_start_time
            now = pygame.time.get_ticks()
            if now - smoke_frame_timer > smoke_frame_interval:
                smoke_frame_timer = now
                smoke_frame_index = (smoke_frame_index + 1) % len(smoke_frames)
        if cylinder_width == 0:
            show_fiend=True
            cigarette = False
            fiend_start_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - fiend_start_time > fiend_duration:
                show_fiend = False

        shrink_fraction = min((total_shrink_time + current_hold) / 7500, 1)  # 7.5 seconds to fully shrink
        cylinder_width = max(cylinder_max_width * (1 - shrink_fraction), 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
