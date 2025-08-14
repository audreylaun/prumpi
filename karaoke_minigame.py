import pygame
import time

def render_multiline_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + ("" if current_line == "" else " ") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines

def karaoke():
    total_coins = 0
    background = pygame.image.load("data/image/saloon_stage.png")
    background = pygame.transform.scale(background, (1000, 700))
    dino = pygame.image.load("data/image/prumpi.png")
    dino = pygame.transform.scale(dino, (300, 400))
    dino_pos = (700, 300)

    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dinosaur Karaoke Minigame")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comic_sansms", 28)
    big_font = pygame.font.SysFont("comic_sansms", 36)
    lyric_font = pygame.font.SysFont("comic_sansms",20)
    button_color = (255, 225, 125)
    button_hover_color = (255, 200, 100)
    text_color = (0, 0, 0)

    lyrics = ("What it is, ho? What's up?\n"
              "Every good girl needs a little thug\n"
              "Every block boy needs a little love\n"
              "If you put it down, I'ma pick it up, up, up")

    lyrics_no_newlines = lyrics.replace("\n", " ")

    input_text = ""
    mode = "start"
    start_time = None
    coins_earned = 0
    elapsed_time = 0

    # Buttons
    begin_button = pygame.Rect(400, 500, 200, 60)
    restart_button = pygame.Rect(780, 20, 180, 60)
    exit_game_button = pygame.Rect(780, 95, 180, 60)
    results_restart_button = pygame.Rect(400, 500, 200, 60)
    end_button = pygame.Rect(400, 600, 200, 60)

    def draw_button(text, rect, mouse_pos):
        if rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=10)
        text_surf = font.render(text, True, text_color)
        screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                                rect.y + (rect.height - text_surf.get_height()) // 2))

    pygame.mixer.music.load('data/audio/whatitis.mp3')
    pygame.mixer.music.play(-1)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.load('data/audio/background_music.mp3')
                pygame.mixer.music.play(-1)
                return 0  # No coins if quit

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == "start" and begin_button.collidepoint(mouse_pos):
                    mode = "typing"
                    start_time = time.time()
                    input_text = ""

                elif mode == "typing":
                    if restart_button.collidepoint(mouse_pos):
                        # Restart typing mode
                        input_text = ""
                        start_time = time.time()
                    elif exit_game_button.collidepoint(mouse_pos):
                        mode = "results"

                elif mode == "results":
                    if results_restart_button.collidepoint(mouse_pos):
                        total_coins += coins_earned
                        mode = "start"
                        input_text = ""
                        coins_earned = 0
                        elapsed_time = 0
                        start_time = None
                    elif end_button.collidepoint(mouse_pos):
                        total_coins += coins_earned
                        pygame.mixer.music.load('data/audio/background_music.mp3')
                        pygame.mixer.music.play(-1)
                        return total_coins

            elif event.type == pygame.KEYDOWN and mode == "typing":
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # Ignore Enter key
                else:
                    input_text += event.unicode

                # Check if finished
                if input_text == lyrics_no_newlines:
                    elapsed_time = time.time() - start_time
                    #CREATE AN ALGORITHM FOR CALCULATING HOW MANY COINS TO GIVE THE USER
                    if elapsed_time <= 30:
                        coins_earned = 100
                    elif elapsed_time >= 120:
                        coins_earned = 10
                    else:
                        coins_earned = int(100 - ((elapsed_time - 30) / 90) * 90)
                    mode = "results"

        if mode == "start":
            title = big_font.render("Karaoke Minigame", True, (0,0,0))
            screen.blit(background, (0, 0))
            screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 150))
            instructions = font.render("Type the lyrics as quickly and accurately as you can for coins!", True, (50,50,50))
            screen.blit(instructions, (screen.get_width()//2 - instructions.get_width()//2, 220))
            draw_button("Begin", begin_button, mouse_pos)

        elif mode == "typing":
            screen.blit(background, (0, 0))
            # Display lyrics at top
            y_offset = 200
            for line in lyrics.split("\n"):
                line_surf = lyric_font.render(line, True, (0,0,0))
                screen.blit(line_surf, (125, y_offset))
                y_offset += line_surf.get_height() + 5

            # Input box (multiline)
            input_box = pygame.Rect(20, 500, 600, 175)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            pygame.draw.rect(screen, (0,0,0), input_box, 2)

            screen.blit(dino, dino_pos)

            lines = render_multiline_text(input_text, font, (0,0,255), input_box.width - 10)
            y_offset = input_box.y + 5
            line_height = font.get_height()
            max_lines = input_box.height // line_height

            for i, line in enumerate(lines[:max_lines]):
                line_surface = font.render(line, True, (0,0,255))
                screen.blit(line_surface, (input_box.x + 5, y_offset + i * line_height))

            # Show correctness feedback
            correct_so_far = lyrics_no_newlines.startswith(input_text)
            if not correct_so_far:
                error_msg = font.render("Typing error! Fix it.", True, (255, 0, 0))
                screen.blit(error_msg, (20, 450))

            # Restart button on the right side of input box
            draw_button("Restart", restart_button, mouse_pos)
            draw_button("Exit game", exit_game_button, mouse_pos)

            # Timer display (top right)
            if start_time is not None:
                elapsed = time.time() - start_time
                timer_surf = font.render(f"Time: {elapsed:.2f}s", True, (0, 0, 0))
                screen.blit(timer_surf, (screen.get_width() - timer_surf.get_width() - 20, 175))

        elif mode == "results":
            result_title = big_font.render("Results", True, (0,0,0))
            screen.blit(result_title, (screen.get_width()//2 - result_title.get_width()//2, 150))

            time_msg = font.render(f"Your time: {elapsed_time:.2f} seconds", True, (0,0,0))
            coins_msg = font.render(f"Coins earned: {coins_earned}", True, (0,0,0))
            screen.blit(time_msg, (screen.get_width()//2 - time_msg.get_width()//2, 250))
            screen.blit(coins_msg, (screen.get_width()//2 - coins_msg.get_width()//2, 300))

            draw_button("Restart", results_restart_button, mouse_pos)
            draw_button("Back to Saloon", end_button, mouse_pos)

        pygame.display.flip()
        clock.tick(60)