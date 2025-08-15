import pygame
import random
import sys
import time

def draw_happiness_meter(screen, happiness, max_happiness):
    meter_x = 20
    meter_y = 200
    meter_width = 30
    meter_height = 300  # total height of the meter

    # Outline
    # Fill height proportional to happiness
    fill_height = int((happiness / max_happiness) * meter_height)
    pygame.draw.rect(
        screen,
        (111, 129, 51), # yellow fill
        (meter_x, meter_y + (meter_height - fill_height), meter_width, fill_height)
    )

    pygame.draw.rect(screen, (0,0,0), (meter_x, meter_y, meter_width, meter_height), 2)
    # pygame.draw.rect(screen, (255, 225, 125), (meter_x, meter_y, meter_width, meter_height))


    icon = pygame.image.load("data/image/smile_meter.png").convert_alpha()
    icon = pygame.transform.scale(icon, (50,50))

    screen.blit(icon, (15,150))

def happiness_minigame():
    pygame.init()

    # --- Screen setup ---
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Coin Catch Minigame")
    clock = pygame.time.Clock()

    # --- Colors ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (255, 225, 125)
    BUTTON_TEXT_COLOR = (24, 100, 24)

    # --- Load images ---
    background = pygame.image.load('data/image/prumpi_world.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    prumpi = pygame.image.load("data/image/coin_prumpi.png")
    prumpi = pygame.transform.scale(prumpi, (200, 200))
    coin_img = pygame.image.load('data/image/coin.png')
    coin_img = pygame.transform.scale(coin_img, (40, 40))

    # --- Player setup ---
    player_rect = prumpi.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    player_speed = 7

    # --- Coin setup ---
    coins = []
    coin_speed = 5
    coin_spawn_rate = 10  # coins per second (adjust if needed)
    total_coins = 0

    # --- Fonts ---
    font = pygame.font.SysFont("comic_sansms", 32)
    big_font = pygame.font.SysFont("comic_sansms", 48)

    # --- WELCOME SCREEN ---
    welcome_text = [
        "You have maxed out your happiness meter!",
        'Use keys "A" and "D" to catch falling coins!',
        "Press any key to start..."
    ]

    waiting = True
    while waiting:
        screen.blit(background, (0, 0))
        for i, line in enumerate(welcome_text):
            text_surf = big_font.render(line, True, BUTTON_COLOR)
            text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50 + i*50))
            screen.blit(text_surf, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return total_coins
            if event.type == pygame.KEYDOWN:
                waiting = False

    # --- MAIN GAME LOOP (20 seconds) ---
    spawn_timer = 0
    start_time = time.time()
    game_duration = 20
    running = True

    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds
        spawn_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Player movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_d] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # --- Spawn coins ---
        while spawn_timer > 1 / coin_spawn_rate:
            spawn_timer -= 1 / coin_spawn_rate
            x_pos = random.randint(0, WIDTH - 40)
            coins.append(coin_img.get_rect(topleft=(x_pos, -40)))

        # --- Move coins ---
        for coin in coins:
            coin.y += coin_speed

        # --- Collision detection ---
        for coin in coins[:]:
            if player_rect.colliderect(coin):
                total_coins += 1
                coins.remove(coin)
            elif coin.top > HEIGHT:
                coins.remove(coin)

        # --- Draw everything ---
        screen.blit(background, (0, 0))
        screen.blit(prumpi, player_rect)
        for coin in coins:
            screen.blit(coin_img, coin)

        # Coin count
        coin_text = font.render(f"Coins: {total_coins}", True, BUTTON_TEXT_COLOR)
        screen.blit(coin_text, (10, 10))

        # Timer
        elapsed_time = time.time() - start_time
        time_left = max(0, int(game_duration - elapsed_time))
        timer_text = font.render(f"Time: {time_left}", True, BUTTON_TEXT_COLOR)
        timer_rect = timer_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(timer_text, timer_rect)

        pygame.display.flip()

        if elapsed_time >= game_duration:
            running = False

    # --- END SCREEN ---
    end_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60)
    end_screen_running = True
    while end_screen_running:
        screen.blit(background, (0, 0))

        # Congratulatory text
        congrats_text = big_font.render(
            f"Congratulations! You earned {total_coins} coins!", True, BUTTON_COLOR)
        congrats_rect = congrats_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(congrats_text, congrats_rect)

        # Draw end button
        pygame.draw.rect(screen, BUTTON_COLOR, end_button_rect)
        button_text = font.render("End", True, BUTTON_TEXT_COLOR)
        button_rect = button_text.get_rect(center=end_button_rect.center)
        screen.blit(button_text, button_rect)

        pygame.display.flip()

        # Handle button click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if end_button_rect.collidepoint(event.pos):
                    end_screen_running = False

    # pygame.quit()
    return total_coins


