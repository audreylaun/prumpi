import pygame
from happiness import draw_happiness_meter

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

    # --- Resize ---
    coin_img = pygame.transform.scale(coin_img, (80,80))
    title_background = pygame.transform.scale(title_background, (1000, 700))
    dino_title = pygame.transform.scale(dino_title, (60,80))
    title_image = pygame.transform.scale(title_image,(500,300))

    # --- Buttons ---
    font = pygame.font.SysFont("comic_sansms", 32)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)
    button_rect_begin = pygame.Rect(screen.get_width() // 2 - 100, 600, 200, 60)
    button_text_begin = font.render("Begin", True, button_text_color)

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
                if screen_mode == "title" and button_rect_begin.collidepoint(mouse_pos):
                    title_sequence = True

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
            screen.fill((180, 220, 255))
            work_text = font.render("Now in WORK mode!", True, (0,0,0))
            screen.blit(work_text, (350, 300))

        pygame.display.flip()
        clock.tick(60)