import pygame, random, time

# Tetris Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]


COLORS = [
    (252, 213, 144), #light yellow
    (174, 196, 132), #olive green
    (143, 156, 191), #light blue
    (237, 187, 211), #light pink
    (196, 177, 159), #tan
    (164, 143, 191) #purple
]

CELL_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 10, 15
PLAYFIELD_WIDTH = GRID_WIDTH * CELL_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * CELL_SIZE

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
PLAYFIELD_X = (WINDOW_WIDTH - PLAYFIELD_WIDTH) // 2
PLAYFIELD_Y = (WINDOW_HEIGHT - PLAYFIELD_HEIGHT) // 2 + 15


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def valid_position(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = off_x + x, off_y + y
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

def join_shape(grid, shape, offset, color_idx):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and 0 <= off_y + y < GRID_HEIGHT:
                grid[off_y + y][off_x + x] = color_idx + 1

def clear_lines(grid):
    lines_cleared = 0
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    while len(new_grid) < GRID_HEIGHT:
        new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return new_grid, lines_cleared

def run_tetris_minigame():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Dino Work")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comic_sansms", 28)
    big_font = pygame.font.SysFont("comic_sansms", 36)
    button_color = (255, 225, 125)
    button_hover_color = (255, 200, 100)
    text_color = (0, 0, 0)

    # Images
    background = pygame.image.load('data/image/box_minigame.png')
    # Resizing images
    background = pygame.transform.scale(background, (1000, 700))

    # GAME STUFF
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    current_piece = random.choice(SHAPES)
    current_color = random.randrange(len(COLORS))
    piece_x, piece_y = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0

    next_piece = random.choice(SHAPES)
    next_color = random.randrange(len(COLORS))


    #Title screen stuff
    title = big_font.render("Box Stack Minigame", True, (0, 0, 0))
    title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10), pygame.SRCALPHA)
    title_bg.fill((255, 225, 125, 180))
    title_x = screen.get_width() // 2 - title.get_width() // 2
    title_y = 250
    instructions = font.render("Use WASD to arrange falling boxes to form complete horizontal lines!", True, (50, 50, 50))
    inst_bg = pygame.Surface((instructions.get_width() + 20, instructions.get_height() + 10), pygame.SRCALPHA)
    inst_bg.fill((255, 225, 125, 180))
    inst_x = screen.get_width() // 2 - instructions.get_width() // 2
    inst_y = 320

    # Buttons
    begin_button = pygame.Rect(400, 500, 200, 60)
    restart_button = pygame.Rect(780, 500, 180, 60)
    exit_game_button = pygame.Rect(780, 575, 180, 60)
    results_restart_button = pygame.Rect(400, 400, 200, 60)
    end_button = pygame.Rect(400, 500, 200, 60)

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


    drop_time, drop_speed = 0, 500
    score = 0
    running = True

    screen_mode = 'title'

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        dt = clock.tick(60)
        drop_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if screen_mode == "game" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if valid_position(grid, current_piece, (piece_x - 1, piece_y)):
                        piece_x -= 1
                elif event.key == pygame.K_d:
                    if valid_position(grid, current_piece, (piece_x + 1, piece_y)):
                        piece_x += 1
                elif event.key == pygame.K_s:
                    if valid_position(grid, current_piece, (piece_x, piece_y + 1)):
                        piece_y += 1
                elif event.key == pygame.K_w:
                    rotated = rotate(current_piece)
                    if valid_position(grid, rotated, (piece_x, piece_y)):
                        current_piece = rotated
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_mode == "title" and begin_button.collidepoint(mouse_pos):
                    screen_mode = "game"
                    start_time = time.time()
                elif screen_mode == "game":
                    if restart_button.collidepoint(mouse_pos):
                        return run_tetris_minigame() #need to change this so it resets within the same call
                    elif exit_game_button.collidepoint(mouse_pos):
                        screen_mode = "results"
                elif screen_mode == "results":
                    if end_button.collidepoint(mouse_pos):
                        return score
                    elif results_restart_button.collidepoint(mouse_pos):
                        return run_tetris_minigame() #need to change this so it resets within the same call

        if drop_time > drop_speed:
            drop_time = 0
            if valid_position(grid, current_piece, (piece_x, piece_y + 1)):
                piece_y += 1
            else:
                join_shape(grid, current_piece, (piece_x, piece_y), current_color)
                grid, lines = clear_lines(grid)
                score += lines * 5

                # Instead of picking random again, use the "next piece"
                current_piece = next_piece
                current_color = next_color
                piece_x, piece_y = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0

                # Roll a new next piece
                next_piece = random.choice(SHAPES)
                next_color = random.randrange(len(COLORS))

                if not valid_position(grid, current_piece, (piece_x, piece_y)):
                    screen_mode = "results"

        # Drawing section
        if screen_mode == "game":
            screen.blit(background, (0,0))
            pygame.draw.rect(screen, (200,200,200), (PLAYFIELD_X, PLAYFIELD_Y, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT),2)
            for x in range(GRID_WIDTH + 1):
                pygame.draw.line(
                    screen, (50, 50, 50),
                    (PLAYFIELD_X + x * CELL_SIZE, PLAYFIELD_Y),
                    (PLAYFIELD_X + x * CELL_SIZE, PLAYFIELD_Y + PLAYFIELD_HEIGHT)
                )
            for y in range(GRID_HEIGHT + 1):
                pygame.draw.line(
                    screen, (50, 50, 50),
                    (PLAYFIELD_X, PLAYFIELD_Y + y * CELL_SIZE),
                    (PLAYFIELD_X + PLAYFIELD_WIDTH, PLAYFIELD_Y + y * CELL_SIZE)
                )

            label = font.render("Next:", True, (255, 255, 255))
            screen.blit(label, (PLAYFIELD_X + PLAYFIELD_WIDTH + 40, PLAYFIELD_Y))

            # Draw the next piece
            for y, row in enumerate(next_piece):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            screen, COLORS[next_color],
                            (PLAYFIELD_X + PLAYFIELD_WIDTH + 100 + x * CELL_SIZE,
                             PLAYFIELD_Y + 40 + y * CELL_SIZE,
                             CELL_SIZE, CELL_SIZE)
                        )

            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if grid[y][x]:
                        color = COLORS[grid[y][x] - 1]
                        pygame.draw.rect(
                            screen, color,
                            (PLAYFIELD_X + x * CELL_SIZE, PLAYFIELD_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        )
            # Draw current piece
            for y, row in enumerate(current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            screen, COLORS[current_color],
                            (PLAYFIELD_X + (piece_x + x) * CELL_SIZE, PLAYFIELD_Y + (piece_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        )

            draw_button("Restart", restart_button, mouse_pos)
            draw_button("Exit game", exit_game_button, mouse_pos)

        elif screen_mode == "title":
            screen.blit(background, (0, 0))
            screen.blit(title_bg, (title_x - 10, title_y - 5))
            screen.blit(title, (title_x, title_y))
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 250))
            screen.blit(inst_bg, (inst_x - 10, inst_y - 5))
            screen.blit(instructions, (inst_x, inst_y))
            draw_button("Begin", begin_button, mouse_pos)

        elif screen_mode == "results":
            screen.blit(background, (0, 0))

            result_title = big_font.render("Results", True, (0, 0, 0))
            screen.blit(result_title, (screen.get_width() // 2 - result_title.get_width() // 2, 150))

            coins_msg = font.render(f"Coins earned: {int(score)}", True, (0, 0, 0))
            screen.blit(coins_msg, (screen.get_width() // 2 - coins_msg.get_width() // 2, 300))

            draw_button("Restart", results_restart_button, mouse_pos)
            draw_button("Back to Work", end_button, mouse_pos)

            # display how many rows you clearned/points you earned
            # prompt if you want to play again

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    run_tetris_minigame()
