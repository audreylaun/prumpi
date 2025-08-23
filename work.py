import pygame
from happiness import draw_happiness_meter
from box_minigame import run_tetris_minigame

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

    # --- Resize ---
    coin_img = pygame.transform.scale(coin_img, (80,80))
    title_background = pygame.transform.scale(title_background, (1000, 700))
    dino_title = pygame.transform.scale(dino_title, (60,80))
    title_image = pygame.transform.scale(title_image,(500,300))
    work_background = pygame.transform.scale(work_background, (1000, 700))
    volume_on_img = pygame.transform.scale(volume_on_img, (60, 60))
    volume_off_img = pygame.transform.scale(volume_off_img, (60, 60))
    prumpi_work = pygame.transform.scale(prumpi_work, (150, 150))

    # --- Buttons ---
    font = pygame.font.SysFont("comic_sansms", 32)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)
    button_rect_begin = pygame.Rect(screen.get_width() // 2 - 100, 600, 200, 60)
    button_text_begin = font.render("Begin", True, button_text_color)

    button_rect_boxes = pygame.Rect(750, 20, 200, 60)
    button_text_boxes = font.render("Stack boxes", True, button_text_color)

    button_rect_world = pygame.Rect(50, 20, 275, 50)
    button_text_world = font.render('Return to World', True, button_text_color)

    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0,0,0))
    coin_button_home = pygame.Rect(35, 600, 60, 60)

    button_volume = pygame.Rect(930, 630, 60, 60)

    # --- Screen Parameters ---
    screen_mode = "title"
    door_rect = pygame.Rect(100, 450, 50, 50)
    title_sequence = False
    dino_pos_title = [400, 475]  # use list for mutability
    dino_speed = 2               # pixels per frame

    running = True
    while running:
        screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                        num_coins += run_tetris_minigame()
                        button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))


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

            screen.blit(prumpi_work, (425, 339))

            if volume_on == True:
                screen.blit(volume_on_img, (button_volume.x, button_volume.y))
            elif volume_on == False:
                screen.blit(volume_off_img, (button_volume.x, button_volume.y))

            pygame.draw.rect(screen, button_color, button_rect_world, border_radius=12)
            screen.blit(button_text_world, (button_rect_world.x, button_rect_world.y))

            pygame.draw.rect(screen, button_color, button_rect_boxes, border_radius=12)
            screen.blit(button_text_boxes, (button_rect_boxes.x, button_rect_boxes.y))

            draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

            screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
            screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))



        pygame.display.flip()
        clock.tick(60)