import pygame
from happiness import draw_happiness_meter

def run_store(num_coins, happiness, bow, gem, backpack, HAPPINESS_MAX, volume_on):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dino Shop")
    clock = pygame.time.Clock()

    # import pictures
    volume_on_img = pygame.image.load("data/image/volume_on.png")
    volume_off_img = pygame.image.load("data/image/volume_off.png")
    coin_img = pygame.image.load("data/image/coin.png")
    shop_screen = pygame.image.load("data/image/shop.png")
    bow_img = pygame.image.load("data/image/bow.png")
    check = pygame.image.load("data/image/check.png")
    gem_img = pygame.image.load("data/image/gem.png")
    backpack_img = pygame.image.load("data/image/backpack.png")
    prumpi_backpack = pygame.image.load("data/image/prumpi_backpack.png")

    #resize pictures
    prumpi_backpack = pygame.transform.scale(prumpi_backpack, (300, 400))
    coin_img = pygame.transform.scale(coin_img, (80, 80))
    shop_screen = pygame.transform.scale(shop_screen, (1000, 700))
    check = pygame.transform.scale(check, (50, 50))

    # --- Set Font and Button Colors  ---
    font = pygame.font.SysFont("comic_sansms", 32)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)

    coin_button_home = pygame.Rect(35, 600, 60, 60)
    coin_button_else = pygame.Rect(35, 35, 60, 60)
    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))


    button_rect_world = pygame.Rect(50, 20, 275, 50)
    button_text_world = font.render('Return to World', True, button_text_color)

    # volume stuff
    volume_on_img = pygame.transform.scale(volume_on_img, (60,60))
    volume_off_img = pygame.transform.scale(volume_off_img, (60,60))
    button_volume = pygame.Rect(930, 630, 60, 60)

    # Shop
    # bow = False
    item_1_rect = pygame.Rect(200, 125, 100, 100)
    item_1_text = font.render('30¢', True, button_text_color)

    # gem = False
    item_2_rect = pygame.Rect(400, 125, 100, 100)
    item_2_text = font.render('50¢', True, button_text_color)

    # backpack = False
    item_3_rect = pygame.Rect(600, 125, 100, 100)
    item_3_text = font.render('100¢', True, button_text_color)

    screen_mode = "home"

    running = True
    while running:
        # screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_mode == "home":
                    if button_rect_world.collidepoint(mouse_pos):
                        return num_coins, bow, gem, backpack, volume_on
                    if button_volume.collidepoint(mouse_pos):
                        if volume_on == True:
                            pygame.mixer.music.set_volume(0)
                            volume_on = False
                        elif volume_on == False:
                            pygame.mixer.music.set_volume(0.5)
                            volume_on = True
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

        if screen_mode == "home":
            screen.blit(shop_screen, (0, 0))
            pygame.draw.rect(screen, button_color, button_rect_world, border_radius=12)
            screen.blit(button_text_world, (button_rect_world.x + 10, button_rect_world.y + 5))

            if volume_on == True:
                screen.blit(volume_on_img, (button_volume.x, button_volume.y))
            elif volume_on == False:
                screen.blit(volume_off_img, (button_volume.x, button_volume.y))

            draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

            bow_img = pygame.transform.scale(bow_img, (100, 100))
            screen.blit(bow_img, (item_1_rect.x, item_1_rect.y))
            if bow == False:
                screen.blit(item_1_text, (item_1_rect.x + 20, item_1_rect.y + 80))
            if bow == True:
                screen.blit(check, (item_1_rect.x + 30, item_1_rect.y + 30))

            gem_img = pygame.transform.scale(gem_img, (75, 75))
            screen.blit(gem_img, (item_2_rect.x + 12.5, item_2_rect.y + 12.5))
            if gem == False:
                screen.blit(item_2_text, (item_2_rect.x + 20, item_2_rect.y + 80))
            if gem == True:
                screen.blit(check, (item_2_rect.x + 30, item_2_rect.y + 30))

            backpack_img = pygame.transform.scale(backpack_img, (100, 100))
            screen.blit(backpack_img, (item_3_rect.x, item_3_rect.y))
            if backpack == False:
                screen.blit(item_3_text, (item_3_rect.x + 20, item_3_rect.y + 80))
            if backpack == True:
                screen.blit(check, (item_3_rect.x + 30, item_3_rect.y + 30))

            screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
            screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

        pygame.display.flip()