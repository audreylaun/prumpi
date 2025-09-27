import pygame
from happiness import draw_happiness_meter, happiness_minigame
from displays import announcement
import random
import time
import pygame
import os

def load_book_images(folder, max_width=800, max_height=600):
    pages = []
    for i in range(1, 12):  # since you have page_1.png ... page_11.png
        path = os.path.join(folder, f"page_{i}.png")
        img = pygame.image.load(path).convert_alpha()

        # scale to fit inside 1000x700 window with margins
        w, h = img.get_size()
        scale = min(max_width / w, max_height / h)
        new_size = (int(w * scale), int(h * scale))
        img = pygame.transform.smoothscale(img, new_size)

        pages.append(img)
    return pages

def run_bedroom_game(num_coins, bow, gem, backpack, labubu, hat, heels, happiness, HAPPINESS_MAX, volume_on, bedroom_first_open, bedroom_first_complete):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dino Home")
    clock = pygame.time.Clock()

    # --- Load images ---
    volume_on_img = pygame.image.load("data/image/volume_on.png")
    volume_off_img = pygame.image.load("data/image/volume_off.png")
    coin_img = pygame.image.load("data/image/coin.png")
    title_background = pygame.image.load("data/image/cabazon.png")
    dino_title = pygame.image.load("data/image/prumpi_standing.png")
    title_image = pygame.image.load("data/image/gift_shop_title.png")
    bedroom_background = pygame.image.load("data/image/bedroom_updated.png")
    prumpi_head = pygame.image.load("data/image/prumpi_work.png")
    speech_right = pygame.image.load("data/image/speech_bubble_right.png")
    quest_log = pygame.image.load("data/image/quest_log.png")
    quest_log_close = pygame.image.load("data/image/quest_log_closed.png")
    prumpi_standing = pygame.image.load("data/image/prumpi_standing.png")
    prumpi_sitting = pygame.image.load("data/image/prumpi.png")
    blush = pygame.image.load("data/image/blush.png")
    book = pygame.image.load("data/image/book.png")
    arrow_right = pygame.image.load("data/image/arrow_right.png")
    arrow_left = pygame.image.load("data/image/arrow_left.png")

    # --- Resize ---
    coin_img = pygame.transform.scale(coin_img, (80, 80))
    title_background = pygame.transform.scale(title_background, (1000, 700))
    title_image = pygame.transform.scale(title_image, (500, 300))
    bedroom_background = pygame.transform.scale(bedroom_background, (1000, 700))
    volume_on_img = pygame.transform.scale(volume_on_img, (60, 60))
    volume_off_img = pygame.transform.scale(volume_off_img, (60, 60))
    speech_right = pygame.transform.scale(speech_right, (375, 100))
    blush = pygame.transform.scale(blush, (200, 100))
    quest_log = pygame.transform.scale(quest_log, (800, 500))
    quest_log_open = pygame.transform.scale(quest_log, (75, 75))
    quest_log_close = pygame.transform.scale(quest_log_close, (50, 75))
    prumpi_standing = pygame.transform.scale(prumpi_standing, (300, 400))
    prumpi_sitting = pygame.transform.scale(prumpi_sitting, (300, 400))
    prumpi_sitting = pygame.transform.flip(prumpi_sitting, True, False)
    book = pygame.transform.scale(book, (125,100))
    arrow_right = pygame.transform.scale(arrow_right, (50,50))
    arrow_left = pygame.transform.scale(arrow_left, (50,50))

    # Accessories
    hat_img = pygame.image.load("data/image/hat.png")
    heel_img = pygame.image.load("data/image/heel.png")
    bow_img = pygame.image.load("data/image/bow.png")
    gem_img = pygame.image.load("data/image/gem.png")
    prumpi_backpack = pygame.image.load("data/image/prumpi_backpack_standing.png")
    labubu_img = pygame.image.load("data/image/labubu.png")
    # Resize
    hat_img = pygame.transform.scale(hat_img, (130, 100))
    hat_img = pygame.transform.flip(hat_img, True, False)
    heel_img = pygame.transform.scale(heel_img, (125, 125))
    heel_img = pygame.transform.flip(heel_img, True, False)
    heel_img = pygame.transform.rotate(heel_img, -45)
    bow_img = pygame.transform.scale(bow_img, (40, 40))
    bow_img = pygame.transform.flip(bow_img, True, False)
    gem_img = pygame.transform.scale(gem_img, (10, 10))
    prumpi_backpack = pygame.transform.scale(prumpi_backpack, (300, 400))
    prumpi_backpack = pygame.transform.flip(prumpi_backpack, True, False)
    labubu_img = pygame.transform.scale(labubu_img, (50, 50))

    # --- Buttons ---
    font = pygame.font.SysFont("comic_sansms", 32)
    font_small = pygame.font.SysFont("comic_sansms", 24)
    font_xsmall = pygame.font.SysFont("comic_sansms", 18)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)
    button_rect_begin = pygame.Rect(screen.get_width() // 2 - 100, 600, 200, 60)
    button_text_begin = font.render("Begin", True, button_text_color)

    button_rect_home = pygame.Rect(700, 20, 250, 60)
    button_text_home = font.render("Return to Bed", True, button_text_color)

    button_rect_game = pygame.Rect(750, 20, 200, 60)
    button_text_game = font.render("TBD", True, button_text_color)

    button_rect_world = pygame.Rect(50, 20, 275, 50)
    button_text_world = font.render('Return to World', True, button_text_color)

    button_rect_log_open = pygame.Rect(462, 15, 75, 75)
    button_rect_log_close = pygame.Rect(475, 610, 50, 75)

    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
    coin_button_home = pygame.Rect(35, 600, 60, 60)

    button_volume = pygame.Rect(930, 630, 60, 60)

    dino_pos = pygame.Rect(100, 150, 300,400)

    # Book stuff
    book_pos = pygame.Rect(415,350,125,100)
    pages = load_book_images("data/book")
    current_page = 0
    left_rect = pygame.Rect(35, 325, 50, 50)
    right_rect = pygame.Rect(910, 325, 50, 50)
    book_complete = False
    mama_text = False

    screen_mode = "bedroom"
    if bedroom_first_open:
        screen_mode = "first open"

    running = True
    pygame.mixer.music.load("data/audio/bedroom.mp3")
    pygame.mixer.music.play(-1)

    while running:
        screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        # Quest variables
        # if num_customers < 20:
        #     quest1 = False
        # else:
        #     quest1 = True
        # if num_rows < 50:
        #     quest2 = False
        # else:
        #     quest2 = True
        # if hydration < 7:
        #     quest3 = False
        # else:
        #     quest3 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_mode not in ["title"] and button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True
                if screen_mode == "bedroom":
                    if button_rect_world.collidepoint(mouse_pos):
                        pygame.mixer.music.load("data/audio/background_music.mp3")
                        pygame.mixer.music.play(-1)
                        return num_coins, happiness, volume_on, bedroom_first_complete
                    elif button_rect_log_open.collidepoint(mouse_pos):
                        screen_mode = "log"
                    elif book_pos.collidepoint(mouse_pos):
                        screen_mode = "book"
                if screen_mode == "log":
                    if button_rect_log_close.collidepoint(mouse_pos):
                        screen_mode = "bedroom"
                if screen_mode == "book":
                    if left_rect.collidepoint(event.pos) and current_page > 0:
                        current_page -= 1
                    elif right_rect.collidepoint(event.pos) and current_page < len(pages) - 1:
                        current_page += 1
                    elif button_rect_home.collidepoint(event.pos):
                        screen_mode = "bedroom"
                        current_page = 0
            elif event.type == pygame.KEYDOWN:
                if screen_mode == "first open":
                    screen_mode = "bedroom"
                # elif screen_mode == "first complete":
                #     screen_mode = current_screen

        #Drawing
        if screen_mode == "bedroom":
            screen.blit(bedroom_background, (0, 0))

            if volume_on == True:
                screen.blit(volume_on_img, (button_volume.x, button_volume.y))
            elif volume_on == False:
                screen.blit(volume_off_img, (button_volume.x, button_volume.y))

            screen.blit(prumpi_sitting, dino_pos)

            screen.blit(book, book_pos)

            pygame.draw.rect(screen, button_color, button_rect_world, border_radius=12)
            screen.blit(button_text_world, (button_rect_world.x, button_rect_world.y))

            pygame.draw.rect(screen, button_color, button_rect_game, border_radius=12)
            screen.blit(button_text_game, (button_rect_game.x, button_rect_game.y))

            draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

            screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
            screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

            screen.blit(quest_log_open, (button_rect_log_open.x, button_rect_log_open.y))

            if book_complete:
                happiness+=5
                mama_text = True
                current_time = pygame.time.get_ticks()
                book_complete = False
            if mama_text and pygame.time.get_ticks() - current_time < 2000:
                speech_pos = (300, 150)
                message_text = "I love my mamas <3"
                screen.blit(speech_right, speech_pos)
                text = font.render(message_text, True, (0, 0, 0))
                screen.blit(text, (speech_pos[0] + 40, speech_pos[1] + 20))
            else:
                mama_text = False
            draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

        elif screen_mode == "log":
            screen.blit(bedroom_background, (0, 0))

            screen.blit(quest_log, (100,100))

            screen.blit(quest_log_close, (button_rect_log_close.x, button_rect_log_close.y))

            quest1_text = font_small.render("Quest 1 Text", True, button_text_color)
            # if 20-num_customers >= 0:
            #     num1 = 20-num_customers
            # else:
            #     num1 = 0
            num1 = 100
            quest_1_subtext = font_xsmall.render(f"{num1} remaining", True, button_text_color)
            quest2_text = font_small.render("Quest 2 Text", True, button_text_color)
            # if 50-num_rows >= 0:
            #     num2 = int(50-num_rows)
            # else:
            #     num2 = 0
            num2 = 100
            quest_2_subtext = font_xsmall.render(f"{num2} remaining", True, button_text_color)
            quest3_text = font_small.render("Quest 3 Text", True, button_text_color)
            # if 7-hydration >=0:
            #     num3 = 7-hydration
            # else:
            #     num3 = 0
            num3 = 100
            quest_3_subtext = font_xsmall.render(f"{num3} remaining", True, button_text_color)

            quest_1_text_pos = (525, 225)
            quest_2_text_pos = (525, 325)
            quest_3_text_pos = (525, 425)

            screen.blit(quest1_text, quest_1_text_pos)
            screen.blit(quest_1_subtext, (quest_1_text_pos[0], quest_1_text_pos[1]+25) )

            screen.blit(quest2_text, quest_2_text_pos)
            screen.blit(quest_2_subtext, (quest_2_text_pos[0], quest_2_text_pos[1]+25) )

            screen.blit(quest3_text, quest_3_text_pos)
            screen.blit(quest_3_subtext, (quest_3_text_pos[0], quest_3_text_pos[1]+25) )
            # if quest1:
            #     pygame.draw.line(screen, button_text_color, (quest_1_text_pos[0], quest_1_text_pos[1] + 15),
            #                      (quest_1_text_pos[0] + 200, quest_1_text_pos[1] + 15), 3)
            # if quest2:
            #     pygame.draw.line(screen, button_text_color, (quest_2_text_pos[0], quest_2_text_pos[1] + 15),
            #                      (quest_2_text_pos[0] + 200, quest_2_text_pos[1] + 15), 3)
            # if quest3:
            #     pygame.draw.line(screen, button_text_color, (quest_3_text_pos[0], quest_3_text_pos[1] + 15),
            #                      (quest_3_text_pos[0] + 200, quest_3_text_pos[1] + 15), 3)

        elif screen_mode == "book":
            screen.blit(bedroom_background, (0, 0))
            # Draw the current page centered
            page = pages[current_page]
            px, py = page.get_size()
            screen.blit(page, ((1000 - px) // 2, (700 - py) // 2))
            if current_page == len(pages)-1:
                book_complete = True

            # Draw navigation buttons (simple rectangles for now)
            screen.blit(arrow_left, left_rect)
            screen.blit(arrow_right, right_rect)
            # pygame.draw.rect(screen, (200, 200, 200), left_rect)
            # pygame.draw.rect(screen, (200, 200, 200), right_rect)

            # Exit button (top-right)
            pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
            screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))

        elif screen_mode == "first open":
            welcome_text_1 = "Finally home!"
            welcome_text_2 = "Let's decompress."
            welcome_text_3 = "Press any key to continue."

            bedroom_first_open = False
            announcement(screen, bedroom_background, welcome_text_1, welcome_text_2, welcome_text_3)

        # elif screen_mode == "first complete":
        #     complete_text_1 = "I've decompressed!"
        #     complete_text_2 = "What's next? Who knows."
        #     complete_text_3 = "Press any key to continue"
        #     bedroom_first_complete = False
        #     announcement(screen, bedroom_background, complete_text_1, complete_text_2, complete_text_3)

        if happiness >= HAPPINESS_MAX:
            happiness=0
            coins_added = happiness_minigame()
            num_coins += coins_added
            button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

        # if work_first_complete and quest1 and quest2 and quest3:
        #     current_screen = screen_mode
        #     screen_mode = 'first complete'
        #     work_first_complete = False

        pygame.display.flip()
        clock.tick(60)
