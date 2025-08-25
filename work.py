import pygame
from happiness import draw_happiness_meter
from box_minigame import run_tetris_minigame
import random

def run_work_game(num_coins, bow, gem, backpack, labubu, happiness, HAPPINESS_MAX, volume_on):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dino Work")
    clock = pygame.time.Clock()

    # --- Load images ---
    volume_on_img = pygame.image.load("data/image/volume_on.png")
    volume_off_img = pygame.image.load("data/image/volume_off.png")
    coin_img = pygame.image.load("data/image/coin.png")
    title_background = pygame.image.load("data/image/cabazon.png")
    dino = pygame.image.load("data/image/prumpi.png")
    dino_title = pygame.image.load("data/image/prumpi_standing.png")
    title_image = pygame.image.load("data/image/gift_shop_title.png")
    work_background = pygame.image.load("data/image/work.png")
    prumpi_work = pygame.image.load("data/image/prumpi_work.png")
    speech_right = pygame.image.load("data/image/speech_bubble_right.png")

    #Customers
    penguin_front = pygame.image.load("data/image/penguin_front.png")
    penguin_back = pygame.image.load("data/image/penguin_back.png")
    sundae_front = pygame.image.load("data/image/sundae_front.png")
    sundae_back = pygame.image.load("data/image/sundae_back.png")
    polly_front = pygame.image.load("data/image/polly_front.png")
    polly_back = pygame.image.load("data/image/polly_back.png")
    boyfriend_front = pygame.image.load("data/image/boyfriend_front.png")
    boyfriend_back = pygame.image.load("data/image/boyfriend_back.png")
    blush = pygame.image.load("data/image/blush.png")


    # --- Resize ---
    coin_img = pygame.transform.scale(coin_img, (80,80))
    title_background = pygame.transform.scale(title_background, (1000, 700))
    dino_title = pygame.transform.scale(dino_title, (60,80))
    title_image = pygame.transform.scale(title_image,(500,300))
    work_background = pygame.transform.scale(work_background, (1000, 700))
    volume_on_img = pygame.transform.scale(volume_on_img, (60, 60))
    volume_off_img = pygame.transform.scale(volume_off_img, (60, 60))
    prumpi_work = pygame.transform.scale(prumpi_work, (150, 150))
    speech_right = pygame.transform.scale(speech_right, (500,100))
    blush = pygame.transform.scale(blush, (200,100))


    #Customers
    penguin_front = pygame.transform.scale(penguin_front, (200,300))
    penguin_back = pygame.transform.scale(penguin_back, (200,300))
    sundae_front = pygame.transform.scale(sundae_front, (200,300))
    sundae_back = pygame.transform.scale(sundae_back, (200,300))
    polly_front = pygame.transform.scale(polly_front, (200,300))
    polly_back = pygame.transform.scale(polly_back, (200,300))
    boyfriend_front = pygame.transform.scale(boyfriend_front, (200,300))
    boyfriend_back = pygame.transform.scale(boyfriend_back, (200,300))


    # --- Buttons ---
    font = pygame.font.SysFont("comic_sansms", 32)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)
    button_rect_begin = pygame.Rect(screen.get_width() // 2 - 100, 600, 200, 60)
    button_text_begin = font.render("Begin", True, button_text_color)

    button_rect_boxes = pygame.Rect(750, 20, 200, 60)
    button_text_boxes = font.render("Clean up shop", True, button_text_color)

    button_rect_world = pygame.Rect(50, 20, 275, 50)
    button_text_world = font.render('Return to World', True, button_text_color)

    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0,0,0))
    coin_button_home = pygame.Rect(35, 600, 60, 60)

    button_volume = pygame.Rect(930, 630, 60, 60)

    #Backpacks on wall
    backpack_1 = pygame.image.load("data/image/backpack.png")
    backpack_2 = pygame.image.load("data/image/backpack_purple.png")
    backpack_3 = pygame.image.load("data/image/backpack_green.png")
    backpack_4 = pygame.image.load("data/image/backpack_orange.png")
    backpack_5 = pygame.image.load("data/image/backpack_yellow.png")
    backpack_6 = pygame.image.load("data/image/backpack_blue.png")

    backpack_1 = pygame.transform.scale(backpack_1, (80,80))
    backpack_2 = pygame.transform.scale(backpack_2, (80,80))
    backpack_3 = pygame.transform.scale(backpack_3, (80,80))
    backpack_4 = pygame.transform.scale(backpack_4, (80,80))
    backpack_5 = pygame.transform.scale(backpack_5, (80,80))
    backpack_6 = pygame.transform.scale(backpack_6, (80,80))

    backpack_1_rect = pygame.Rect(380, 100, 80, 80)
    backpack_2_rect = pygame.Rect(460, 100, 80, 80)
    backpack_3_rect = pygame.Rect(540, 100, 80, 80)
    backpack_4_rect = pygame.Rect(380, 200, 80, 80)
    backpack_5_rect = pygame.Rect(460, 200, 80, 80)
    backpack_6_rect = pygame.Rect(540, 200, 80, 80)

    backpacks = [("pink", backpack_1, backpack_1_rect),
                 ("purple", backpack_2, backpack_2_rect),
                 ("green", backpack_3, backpack_3_rect),
                 ("orange", backpack_4, backpack_4_rect),
                 ("yellow", backpack_5, backpack_5_rect),
                 ("blue", backpack_6, backpack_6_rect)]

    # --- Screen Parameters ---
    screen_mode = "title"
    door_rect = pygame.Rect(100, 450, 50, 50)
    title_sequence = False
    dino_pos_title = [400, 475]
    dino_pos_work = (425, 339)
    dino_speed = 2


    customer_present = False
    customer_pos_start = [0,400]
    customer_pos_active = customer_pos_start.copy()
    customer_rect_counter = pygame.Rect(350, 400, 100, 300)
    walk_in = False
    walk_out = False
    request = False
    dragging_backpack = None
    drag_offset = (0, 0)
    customer_request = None
    message_text = None
    current_customer = None  # persists across frames

    customer_interval = 15000
    last_customer_time = 0

    customer_list  = ["sundae", "polly", "penguin", "boyfriend"]

    customers = {"sundae": [sundae_front, sundae_back],
                 "polly": [polly_front, polly_back],
                 "penguin": [penguin_front, penguin_back],
                 "boyfriend": [boyfriend_front, boyfriend_back],}

    running = True
    while running:
        screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return num_coins, happiness, volume_on
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen not in ["title"] and button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True
                if screen_mode == "title" and button_rect_begin.collidepoint(mouse_pos):
                    title_sequence = True
                if screen_mode == "work":
                    if button_rect_world.collidepoint(mouse_pos):
                        mode = "exit"
                        return num_coins, happiness, volume_on
                    elif button_rect_boxes.collidepoint(mouse_pos):
                        num_coins += run_tetris_minigame(0)
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
                    if request:
                        for color, img, rect in backpacks:
                            if rect.collidepoint(mouse_pos):
                                dragging_backpack = (color, img, rect.copy())  # save original rect
                                drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if screen_mode == "work":
                    if request:
                        if dragging_backpack:
                            color, img, original_rect = dragging_backpack
                            drop_rect = pygame.Rect(mouse_pos[0] - drag_offset[0], mouse_pos[1] - drag_offset[1],
                                                    original_rect.w, original_rect.h)
                            # check if dropped in customer rect
                            if request and customer_rect.colliderect(drop_rect):
                                if color == customer_request:
                                    message_text = "Perfect! Thank you, Prumpi!"
                                    num_coins += 5
                                    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

                                    request = False
                                    walk_out = True
                                else:
                                    message_text = "That's not the right one!"
                                    original_rect.topleft = (original_rect.x, original_rect.y)
                            dragging_backpack = None

        if screen_mode == "title" and title_sequence:
            # move dinosaur toward door
            if dino_pos_title[0] > door_rect.x:
                dino_pos_title[0] -= dino_speed
            if dino_pos_title[1] < door_rect.y:
                dino_pos_title[1] += dino_speed
            # check collision with door
            dino_rect = pygame.Rect(dino_pos_title[0], dino_pos_title[1], 60, 80)
            if dino_rect.colliderect(door_rect):
                screen_mode = "work"
                title_sequence = False

        if screen_mode == "work" and customer_present:
            if walk_in:
                if customer_pos_active[0] < customer_rect_counter.x:
                    customer_pos_active[0] += dino_speed
                customer_rect = pygame.Rect(customer_pos_active[0], customer_pos_active[1], 200,300)
                if customer_rect.colliderect(customer_rect_counter):
                    request = True
                    walk_in = False
                    customer_request = random.choice(backpacks)[0]
                    message_text = f"I want the {customer_request} backpack!"
            if walk_out:
                if customer_pos_active[0] > customer_pos_start[0]:
                    customer_pos_active[0] -= dino_speed
                else:
                    walk_out = False
                    customer_present = False
                    customer_pos_active = customer_pos_start.copy()
                    message_text = None

        if dragging_backpack:
            color, img, rect = dragging_backpack
            rect.x = mouse_pos[0] - drag_offset[0]
            rect.y = mouse_pos[1] - drag_offset[1]

        current_time = pygame.time.get_ticks()
        if screen_mode == "work" and not (walk_in or request or walk_out):
            if current_time - last_customer_time >= customer_interval:
                customer_present = True
                customer_pos_active = customer_pos_start.copy()
                walk_in = True
                walk_out = False
                request = False
                last_customer_time = current_time

                current_customer = random.choice(customer_list)

        # --- Drawing ---
        if screen_mode == "title":
            screen.blit(title_background, (0, 0))
            screen.blit(dino_title, dino_pos_title)

            title_rect = title_image.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(title_image, title_rect)

            pygame.draw.rect(screen, button_color, button_rect_begin, border_radius=10)
            pygame.draw.rect(screen, button_color, button_rect_begin, width=2, border_radius=10)
            screen.blit(button_text_begin, (button_rect_begin.x + 60, button_rect_begin.y + 5))

        elif screen_mode == "work":
            screen.blit(work_background, (0, 0))

            screen.blit(prumpi_work, dino_pos_work)

            if volume_on == True:
                screen.blit(volume_on_img, (button_volume.x, button_volume.y))
            elif volume_on == False:
                screen.blit(volume_off_img, (button_volume.x, button_volume.y))

            pygame.draw.rect(screen, button_color, button_rect_world, border_radius=12)
            screen.blit(button_text_world, (button_rect_world.x, button_rect_world.y))

            pygame.draw.rect(screen, button_color, button_rect_boxes, border_radius=12)
            screen.blit(button_text_boxes, (button_rect_boxes.x, button_rect_boxes.y))

            screen.blit(backpack_1, (backpack_1_rect.x, backpack_1_rect.y))
            screen.blit(backpack_2, (backpack_2_rect.x, backpack_2_rect.y))
            screen.blit(backpack_3, (backpack_3_rect.x, backpack_3_rect.y))
            screen.blit(backpack_4, (backpack_4_rect.x, backpack_4_rect.y))
            screen.blit(backpack_5, (backpack_5_rect.x, backpack_5_rect.y))
            screen.blit(backpack_6, (backpack_6_rect.x, backpack_6_rect.y))

            if customer_present:
                if walk_in:
                    customer = customers[current_customer][1]
                if walk_out:
                    customer = customers[current_customer][0]
                screen.blit(customer, customer_pos_active)
                if current_customer == "boyfriend":
                    screen.blit(blush, (300, 375))

            # Draw dragging backpack on top
            if dragging_backpack:
                _, img, rect = dragging_backpack
                screen.blit(img, rect)

            # Draw penguin message
            if message_text:
                speech_pos = (300, 275)
                screen.blit(speech_right, speech_pos)
                text = font.render(message_text, True, (0, 0, 0))
                screen.blit(text, (speech_pos[0] + 40, speech_pos[1] + 20))
            draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

            screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
            screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

        pygame.display.flip()
        clock.tick(60)