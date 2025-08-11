import pygame
import random

pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Salon - Rhythm Mini-Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
YELLOW = (255, 255, 150)
GREEN = (150, 255, 150)
RED = (255, 150, 150)

# --- Parameters ---
NOTE_RADIUS = 30
TARGET_Y = int(HEIGHT * 0.6)
HIT_RANGE = 40
START_SPEED = 3
SPEEDUP_INTERVAL = 15000  # ms
NOTE_INTERVAL = 800

# --- Key mapping ---
KEYS = {
    pygame.K_w: "up",
    pygame.K_a: "left",
    pygame.K_s: "down",
    pygame.K_d: "right"
}

# background image
background = pygame.image.load("data/image/stage.png")
background = pygame.transform.scale(background, (1000, 700))

#prumpi stuff
prumpi_standing = pygame.image.load("data/image/prumpi_standing.png")
# prumpi_standing = pygame.image.load("prumpi.png")
prumpi_squatting = pygame.image.load("data/image/prumpi_squatting.png")

prumpi_standing = pygame.transform.scale(prumpi_standing, (300, 400))
prumpi_squatting = pygame.transform.scale(prumpi_squatting, (300, 400))

prumpi_position = dino_pos = (375, 300)

# --- Load arrow images ---
arrow_images = {
    "left": pygame.image.load("data/image/arrow_left.png").convert_alpha(),
    "right": pygame.image.load("data/image/arrow_right.png").convert_alpha(),
    "up": pygame.image.load("data/image/arrow_up.png").convert_alpha(),
    "down": pygame.image.load("data/image/arrow_down.png").convert_alpha()
}
font = pygame.font.SysFont("comic_sansms", 32)
button_color = (255, 225, 125)
button_text_color = (24, 100, 24)

coin_img = pygame.image.load("data/image/coin.png")
coin_img = pygame.transform.scale(coin_img, (80,80))
coin_button_home = pygame.Rect(35, 600, 60, 60)

# Optional: scale them to fit the note circles
ARROW_SIZE = 60
for key in arrow_images:
    arrow_images[key] = pygame.transform.smoothscale(arrow_images[key], (ARROW_SIZE, ARROW_SIZE))

# --- Note class ---
class Note:
    def __init__(self, direction, y=0):
        self.direction = direction
        lane_offsets = {"up": -200, "left": -100, "right": 100, "down": 200}
        self.x = WIDTH//2 + lane_offsets[direction]
        self.y = y

    def update(self, speed):
        self.y += speed

    def draw(self, surface):
        pygame.draw.circle(surface, GREY, (self.x, int(self.y)), NOTE_RADIUS)
        rect = arrow_images[self.direction].get_rect(center=(self.x, int(self.y)))
        surface.blit(arrow_images[self.direction], rect)

# --- Button helper ---
def draw_button(text, x, y, w, h, color, hover_color, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    is_hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if is_hovered else color, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect, is_hovered

# --- Rhythm game function ---
def rhythm_game():
    clock = pygame.time.Clock()
    score = 0
    notes = []
    note_timer = 0
    speed = START_SPEED
    last_speedup_time = pygame.time.get_ticks()
    button_text_coin = font.render(str(score) + " Prumpi Coins Earned", True, (0, 0, 0))
    prumpi_image = prumpi_standing
    pose_timer = 0  # counts how long squatting pose lasts
    POSE_DURATION = 150  # milliseconds
    running = True
    while running:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # End game entirely
            elif event.type == pygame.KEYDOWN:
                if event.key in KEYS:
                    hit_note = None
                    for note in notes:
                        if note.direction == KEYS[event.key] and abs(note.y - TARGET_Y) <= HIT_RANGE:
                            hit_note = note
                            break
                    if hit_note:
                        notes.remove(hit_note)
                        button_text_coin = font.render(str(score) + " Prumpi Coins", True, (0, 0, 0))
                        score += 1
                        prumpi_image = prumpi_squatting  # change to squat pose
                        pose_timer = pygame.time.get_ticks()  # record when we changed
                    else:
                        running = False  # Miss = end game

        # Spawn new notes
        note_timer += dt
        if note_timer >= NOTE_INTERVAL:
            note_timer = 0
            direction = random.choice(["up", "down", "left", "right"])
            notes.append(Note(direction))

        # Speed up every 15 seconds
        if current_time - last_speedup_time >= SPEEDUP_INTERVAL:
            speed += 1
            last_speedup_time = current_time

        # Update notes
        for note in notes:
            note.update(speed)

        # Missed note check
        for note in notes:
            if note.y - TARGET_Y > HIT_RANGE:
                running = False
                break
        if prumpi_image == prumpi_squatting:
            if pygame.time.get_ticks() - pose_timer > POSE_DURATION:
                prumpi_image = prumpi_standing

        # --- Drawing ---
        screen.blit(background, (0,0))
        screen.blit(prumpi_image, dino_pos)
        pygame.draw.line(screen, BLACK, (0, TARGET_Y), (WIDTH, TARGET_Y), 3)
        for note in notes:
            note.draw(screen)
        screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
        screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

        pygame.display.flip()

    return score

# --- Minigame menu loop ---
def twerk_minigame_menu():
    clock = pygame.time.Clock()
    mode = "start"
    earned_coins = 0

    while True:
        screen.blit(background, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "start" and start_btn.collidepoint(mouse_pos):
                    earned_coins = rhythm_game()
                    mode = "end"
                elif mode == "end":
                    if yes_btn.collidepoint(mouse_pos):
                        earned_coins = rhythm_game()
                    elif no_btn.collidepoint(mouse_pos):
                        return earned_coins, True

        screen.blit(background, (0,0))

        if mode == "start":
            title = font.render("Twerk Mini-Game", True, button_text_color)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            subtitle = font.render("Use keys WASD to twerk to the beat.", True, button_text_color)
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 300))
            start_btn, _ = draw_button("Play", WIDTH//2 - 100, 400, 200, 60, YELLOW, GREEN, mouse_pos)

        elif mode == "end":
            msg = font.render(f"You earned {earned_coins} Prumpi Coins!", True, button_text_color)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
            question = font.render("Play again?", True, button_text_color)
            screen.blit(question, (WIDTH//2 - question.get_width()//2, 270))

            yes_btn, _ = draw_button("Yes", WIDTH//2 - 150, 400, 120, 60, GREEN, YELLOW, mouse_pos)
            no_btn, _ = draw_button("No", WIDTH//2 + 30, 400, 120, 60, RED, YELLOW, mouse_pos)

        pygame.display.flip()
        clock.tick(60)