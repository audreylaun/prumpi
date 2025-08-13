import pygame
import sys
import random
from collections import deque
from dance_minigame import twerk_minigame_menu
from karaoke_minigame import karaoke

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

def run_saloon_game(num_coins):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dino Rugged Saloon")
    clock = pygame.time.Clock()

    # --- Load images ---
    background = pygame.image.load("data/image/saloon.png")
    dino = pygame.image.load("data/image/prumpi.png")
    title_image = pygame.image.load("data/image/saloon_title.png")
    sloth_bar = pygame.image.load("data/image/sloth_bar.png")
    door_left = pygame.image.load("data/image/door_left.png")
    door_right = pygame.image.load("data/image/door_right.png")
    alley_screen = pygame.image.load("data/image/alley.png")
    coin_img = pygame.image.load("data/image/coin.png")
    volume_on_img = pygame.image.load("data/image/volume_on.png")
    volume_off_img = pygame.image.load("data/image/volume_off.png")


    # --- Resize images ---
    background = pygame.transform.scale(background, (1000, 700))
    dino = pygame.transform.scale(dino, (300, 400))
    title_image = pygame.transform.scale(title_image, (500, 300))
    door_left = pygame.transform.scale(door_left, (500, 1000))
    door_right = pygame.transform.scale(door_right, (500, 1000))
    sloth_bar = pygame.transform.scale(sloth_bar, (200,200))
    alley_screen = pygame.transform.scale(alley_screen, (1000, 700))
    coin_img = pygame.transform.scale(coin_img, (80, 80))
    volume_on_img = pygame.transform.scale(volume_on_img, (60, 60))
    volume_off_img = pygame.transform.scale(volume_off_img, (60, 60))
    button_volume = pygame.Rect(930, 630, 60, 60)
    volume_on = True

    # --- Set Font and Button Colors  ---
    font = pygame.font.SysFont("comic_sansms", 32)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)

    # --- Create buttons ---
    # All screens
    button_rect_begin = pygame.Rect(400, 500, 200, 60)
    button_text_begin = font.render("Begin", True, button_text_color)

    button_rect_home = pygame.Rect(700, 30, 250, 60)
    button_text_home = font.render("Return Home", True, button_text_color)

    button_rect_title = title_image.get_rect(center=(screen.get_width() // 2, 300))
    button_rect_alley = pygame.Rect(50, 100, 100, 50)
    button_text_alley = font.render('Break', True, button_text_color)

    button_volume = pygame.Rect(930, 630, 60, 60)

    shrink_button_rect = pygame.Rect(30, 630, 140, 50)
    button_rect_be_naughty = pygame.Rect(675, 550, 300, 60)
    button_text_be_naughty = font.render("Be naughty... (15¢)", True, button_text_color)

    coin_button_home = pygame.Rect(35, 600, 60, 60)
    coin_button_else = pygame.Rect(35, 35, 60, 60)
    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

    button_rect_world = pygame.Rect(50, 20, 275, 50)
    button_text_world = font.render('Return to World', True, button_text_color)

    button_rect_karaoke = pygame.Rect(750, 20, 200, 60)
    button_text_karaoke = font.render("Karaoke", True, button_text_color)

    # --- Variables ---
    screen_mode = "title"
    dino_pos = (640, 165)
    sloth_bar_pos = (400,175)
    running = True
    door_angle = 0  # For swinging animation
    door_animation_speed = 3  # Degrees per frame


    # --- Alley stuff ---
    # Alley transition
    exit_sound = pygame.mixer.Sound("data/audio/exit_sequence.mp3")
    transition_start_time = None
    exit_sound_playing = False
    # Alley
    dino_pos_alley = (315, 250)
    cylinder_max_width = 250  # used to be 300
    cylinder_height = 40
    cylinder_width = cylinder_max_width
    cylinder_orig_pos = (110, 450)
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
        img = pygame.image.load(f"data/image/smoke_{i + 1}.png").convert_alpha()
        img = pygame.transform.scale(img, (50, 50))  # resize as needed
        smoke_frames.append(img)
    smoke_frame_index = 0
    smoke_frame_timer = 0
    smoke_frame_interval = 100  # milliseconds per frame

    # Music
    pygame.mixer.music.load("data/audio/background_music.mp3")
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0

    while running:
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
                if screen_mode == "home":
                    if button_rect_alley.collidepoint(mouse_pos):
                        pygame.mixer.music.fadeout(1000)
                        fade_to_black(screen, clock, background, speed=5)
                        screen_mode = "alley_transition"
                        exit_sound.play()
                        exit_sound_playing = True
                    elif button_rect_karaoke.collidepoint(mouse_pos):
                        num_coins += karaoke()
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

                    elif button_rect_world.collidepoint(mouse_pos):
                        mode = "exit"
                        return num_coins

                elif screen_mode == "title" and button_rect_begin.collidepoint(mouse_pos):
                    screen_mode = "door_animation"

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
                        if int(num_coins) >= 15:
                            cigarette = True
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
                            # Print that you need more coins for that...
                            None

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if screen_mode == "alley":
                    if shrinking:
                        # Add how long it was held this time
                        time_held = pygame.time.get_ticks() - shrink_start_time
                        total_shrink_time += time_held
                        shrinking = False
                        shrink_start_time = None

        # --- Drawing ---
        screen.blit(background, (0, 0))

        if screen_mode == "title":
            door_left_rect = pygame.Rect(500-door_left.get_width(), -150, 500,1000)
            door_right_rect = pygame.Rect(500, -150, 500, 1000)

            screen.blit(door_left, door_left_rect)
            screen.blit(door_right, door_right_rect)

            screen.blit(title_image, button_rect_title)

            pygame.draw.rect(screen, button_color, button_rect_begin, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), button_rect_begin, width=2, border_radius=10)
            screen.blit(button_text_begin, (button_rect_begin.x + 60, button_rect_begin.y + 5))


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
            screen.blit(alley_screen, (0, 0))
            pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
            screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))
            screen.blit(dino, dino_pos_alley)
            if num_coins < 15:
                this_button_color = (180, 170, 140)
            else:
                this_button_color = button_color
            pygame.draw.rect(screen, this_button_color, button_rect_be_naughty, border_radius=12)
            screen.blit(button_text_be_naughty, (button_rect_be_naughty.x, button_rect_be_naughty.y))

            screen.blit(coin_img, (coin_button_else.x, coin_button_else.y))
            screen.blit(button_text_coin, (coin_button_else.x + 100, coin_button_else.y + 20))

            # if backpack:
            #     screen.blit(prumpi_backpack, dino_pos_alley)
            # if bow:
            #     bow_img = pygame.transform.scale(bow_img, (40, 40))
            #     screen.blit(bow_img, (475, 300))
            # if gem:
            #     gem_img = pygame.transform.scale(gem_img, (10, 10))
            #     screen.blit(gem_img, (397, 399))

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


        elif screen_mode == "door_animation":

            # Move doors apart horizontally
            door_angle += door_animation_speed  # We'll re-use this as a frame counter
            slide_distance = door_angle * 5  # 5 pixels per frame

            # Starting positions (closed)
            left_x = 500 - door_left.get_width()
            right_x = 500

            # Apply slide
            left_x -= slide_distance
            right_x += slide_distance

            # Draw the doors at new positions
            screen.blit(door_left, (left_x, 350 - door_left.get_height() // 2))
            screen.blit(door_right, (right_x, 350 - door_right.get_height() // 2))

            # Stop animation after they slide far enough
            if slide_distance >= door_left.get_width():
                screen_mode = "home"

        elif screen_mode == "home":
            screen.blit(dino, dino_pos)
            screen.blit(sloth_bar, sloth_bar_pos)

            pygame.draw.rect(screen, button_color, button_rect_world, border_radius=12)
            screen.blit(button_text_world, (button_rect_world.x, button_rect_world.y))

            pygame.draw.rect(screen, button_color, button_rect_alley, border_radius=12)
            screen.blit(button_text_alley, (button_rect_alley.x, button_rect_alley.y))

            pygame.draw.rect(screen, button_color, button_rect_karaoke, border_radius=12)
            screen.blit(button_text_karaoke, (button_rect_karaoke.x + 20, button_rect_karaoke.y + 10))

            if volume_on == True:
                screen.blit(volume_on_img, (button_volume.x, button_volume.y))
            elif volume_on == False:
                screen.blit(volume_off_img, (button_volume.x, button_volume.y))

            screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
            screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

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
                show_fiend = True
                cigarette = False
                fiend_start_time = pygame.time.get_ticks()
                if pygame.time.get_ticks() - fiend_start_time > fiend_duration:
                    show_fiend = False

            shrink_fraction = min((total_shrink_time + current_hold) / 7500, 1)  # 7.5 seconds to fully shrink
            cylinder_width = max(cylinder_max_width * (1 - shrink_fraction), 0)

        pygame.display.flip()
        clock.tick(60)

    # return "minigame_finished"

# If you want to run it standalone
if __name__ == "__main__":
    run_saloon_game(100)