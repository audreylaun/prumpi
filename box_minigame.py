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
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0)
]

CELL_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20
PLAYFIELD_WIDTH = GRID_WIDTH * CELL_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * CELL_SIZE

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
PLAYFIELD_X = (WINDOW_WIDTH - PLAYFIELD_WIDTH) // 2
PLAYFIELD_Y = (WINDOW_HEIGHT - PLAYFIELD_HEIGHT) // 2

#Images
background = pygame.image.load('data/image/box_stack_background.png')

#Resizing images
background = pygame.transform.scale(background, (1000,700))

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

def run_tetris_minigame(screen, clock):

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    current_piece = random.choice(SHAPES)
    current_color = random.randrange(len(COLORS))
    piece_x, piece_y = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0

    drop_time, drop_speed = 0, 500
    score = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        dt = clock.tick(60)
        drop_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
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

        if drop_time > drop_speed:
            drop_time = 0
            if valid_position(grid, current_piece, (piece_x, piece_y + 1)):
                piece_y += 1
            else:
                join_shape(grid, current_piece, (piece_x, piece_y), current_color)
                grid, lines = clear_lines(grid)
                score += lines * 100
                current_piece = random.choice(SHAPES)
                current_color = random.randrange(len(COLORS))
                piece_x, piece_y = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0
                if not valid_position(grid, current_piece, (piece_x, piece_y)):
                    running = False

        # Draw grid
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

        pygame.display.flip()

    pygame.quit()
    return {"score": score}

def box_minigame():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris Minigame")
    clock = pygame.time.Clock()



    run_tetris_minigame(screen, clock)

if __name__ == "__main__":
    box_minigame()
