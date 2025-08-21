from saloon import run_saloon_game
from salon import run_salon_game
from happiness import draw_happiness_meter, happiness_minigame
import pygame
from store import run_store


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

 # --- Initialize Game ---
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Prumpi World")
clock = pygame.time.Clock()
num_coins = 500
bow = False
gem = False
backpack = False
labubu = False

happiness = 0
HAPPINESS_MAX = 30

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

# --- Rescale images ---
background = pygame.transform.scale(background, (1000, 700))
title_image = pygame.transform.scale(title_image, (500, 300))
pin = pygame.transform.scale(pin, (100,100))
coin_img = pygame.transform.scale(coin_img, (80, 80))

# --- Create buttons ---
button_rect_begin = pygame.Rect(400, 500, 200, 60)
button_text_begin = font.render("Begin", True, button_text_color)

button_rect_salon = pygame.Rect(100, 400, 100, 100)
button_rect_saloon = pygame.Rect(500, 350, 100, 100)
button_rect_shop = pygame.Rect(700, 500, 100, 100)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if screen_mode == "title":
                if button_rect_begin.collidepoint(mouse_pos):
                    screen_mode = "home"
            if screen_mode == "home":
                if button_rect_salon.collidepoint(mouse_pos):
                    num_coins, happiness, volume_on = run_salon_game(num_coins, happiness, bow, gem, backpack, labubu, HAPPINESS_MAX, volume_on)
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                elif button_rect_saloon.collidepoint(mouse_pos):
                    num_coins, happiness, volume_on = run_saloon_game(num_coins, bow, gem, backpack, labubu, happiness, HAPPINESS_MAX, volume_on)
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                elif button_rect_shop.collidepoint(mouse_pos):
                    num_coins, happiness, bow, gem, backpack, labubu, volume_on = run_store(num_coins, happiness, bow, gem, backpack, labubu, HAPPINESS_MAX, volume_on)
                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))


                elif button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True

               #display pins, which will tell you the names of the worlds if you hover over them

    # --- Drawing ---
    if screen_mode == "title":
        screen.blit(background, (0, 0))

        screen.blit(title_image, button_rect_title)

        pygame.draw.rect(screen, button_color, button_rect_begin, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect_begin, width=2, border_radius=10)
        screen.blit(button_text_begin, (button_rect_begin.x + 60, button_rect_begin.y + 5))

    elif screen_mode == "home":
        screen.blit(background, (0,0))
        screen.blit(pin, button_rect_salon)
        screen.blit(pin, button_rect_saloon)
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
            (button_rect_shop, "Go to Shop")
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
                # Position the rect relative to the pin rect
                tooltip_bg_rect.centerx = rect.centerx
                tooltip_bg_rect.bottom = rect.top - 5  # slightly above the pin
                # Draw a rounded rectangle directly on the main screen
                pygame.draw.rect(screen, button_color, tooltip_bg_rect, border_radius=8)
                # Draw the tooltip text on top of the rounded rect, with some padding
                screen.blit(tooltip_surf, (tooltip_bg_rect.x + 5, tooltip_bg_rect.y + 3))


    pygame.display.flip()
    clock.tick(60)