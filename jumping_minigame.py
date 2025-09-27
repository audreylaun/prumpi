import pygame
import random

# --------- CONFIG ----------
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Dino
DINO_W, DINO_H = 44, 44
DINO_X = 50
JUMP_V = -12
GRAVITY = 0.6
DUCK_H = 28

# Obstacles
CACTUS_MIN_GAP = 220
CACTUS_MAX_GAP = 420
CACTUS_SPEED_BASE = 6
SPEED_INCREASE_EVERY = 100  # score points

# Visual
FONT_NAME = None


# Background
BG_IMG = pygame.image.load("data/image/computer_close.png")
BG_IMG = pygame.transform.scale(BG_IMG, (1000, 700))
BG_RECT = BG_IMG.get_rect()

# Customize this rectangle to fit the screen in the computer image
GAME_SCREEN_X = 150
GAME_SCREEN_Y = 120
GAME_SCREEN_W = 700
GAME_SCREEN_H = 400
GROUND_Y = GAME_SCREEN_H - 100  # ground relative to game surface

# Sprites
TREX_IMG = pygame.image.load("data/image/t-rex.png")
TREX_IMG = pygame.transform.scale(TREX_IMG, (DINO_W, DINO_H))
TREX_DUCK_IMG = pygame.transform.scale(TREX_IMG, (DINO_W, DUCK_H))

CACTUS_IMG = pygame.image.load("data/image/cactus.png")
PTERO_IMG = pygame.image.load("data/image/pterodactyl.png")
PTERO_IMG = pygame.transform.scale(PTERO_IMG, (46, 30))



# ---------------------------

class Dino:
    def __init__(self):
        self.x = DINO_X
        self.y = GROUND_Y - DINO_H
        self.w = DINO_W
        self.h = DINO_H
        self.vel_y = 0
        self.on_ground = True
        self.ducking = False
        self.dead = False
        self.anim_timer = 0
        self.anim_frame = 0

    def rect(self):
        if self.ducking:
            return pygame.Rect(self.x, self.y + (DINO_H - DUCK_H), self.w, DUCK_H)
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def jump(self):
        if self.on_ground and not self.dead:
            self.vel_y = JUMP_V
            self.on_ground = False

    def duck(self, start):
        if not self.dead:
            self.ducking = start and self.on_ground

    def update(self):
        if self.dead:
            return
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.y += self.vel_y
            if self.y >= GROUND_Y - self.h:
                self.y = GROUND_Y - self.h
                self.vel_y = 0
                self.on_ground = True
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

    def draw(self, surf):
        r = self.rect()
        if self.ducking:
            surf.blit(TREX_DUCK_IMG, (r.x, r.y))
        else:
            surf.blit(TREX_IMG, (r.x, r.y))


class Cactus:
    def __init__(self, x, speed, width=None, height=None):
        self.img = CACTUS_IMG
        self.width = width if width else self.img.get_width()
        self.height = height if height else self.img.get_height()
        self.x = x
        self.speed = speed
        self.scaled_img = pygame.transform.scale(self.img, (self.width, self.height))

    def rect(self):
        return pygame.Rect(int(self.x), GROUND_Y - self.height, self.width, self.height)

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, surf):
        surf.blit(self.scaled_img, (int(self.x), GROUND_Y - self.height))


class Ptero:
    def __init__(self, x, speed):
        self.img = PTERO_IMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x
        # fly at 10–30% above ground
        self.y = random.randint(GROUND_Y - int(GAME_SCREEN_H*0.3), GROUND_Y - int(GAME_SCREEN_H*0.1))
        self.speed = speed


    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, surf):
        surf.blit(self.img, (int(self.x), int(self.y)))


class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.w = random.randint(30, 60)

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, surf):
        pygame.draw.ellipse(surf, (220, 220, 220), (int(self.x), int(self.y), self.w, 16))


def spawn_cactus(after_x, speed):
    gap = random.randint(CACTUS_MIN_GAP, CACTUS_MAX_GAP)
    # scale relative to GAME_SCREEN_H
    min_scale = 0.1  # 10% of game height
    max_scale = 0.2  # 20% of game height
    height = random.randint(int(GAME_SCREEN_H * min_scale), int(GAME_SCREEN_H * max_scale))
    width = int(CACTUS_IMG.get_width() * (height / CACTUS_IMG.get_height()))
    return Cactus(after_x + gap, speed, width, height)



def spawn_ptero(after_x, speed):
    gap = random.randint(CACTUS_MIN_GAP, CACTUS_MAX_GAP)
    return Ptero(after_x + gap, speed)


def run_trex(surface=None, width=WIDTH, height=HEIGHT):
    pygame.init()
    own_screen = False
    if surface is None:
        screen = pygame.display.set_mode((width, height))
        own_screen = True
    else:
        screen = surface

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comic_sansms", 24)
    button_color = (255, 225, 125)
    button_text_color = (24, 100, 24)

    # Create separate surface for the game area
    game_surface = pygame.Surface((GAME_SCREEN_W, GAME_SCREEN_H))

    dino = Dino()
    obstacles = [spawn_cactus(GAME_SCREEN_W + 60, CACTUS_SPEED_BASE)]
    clouds = [Cloud(GAME_SCREEN_W + i * 150, 30 + i * 20, 0.2 + i * 0.05) for i in range(3)]
    score = 0
    high_score = 0
    total_score = 0
    base_speed = CACTUS_SPEED_BASE
    speed = base_speed
    game_over = False
    started = False
    ground_offset = 0
    dash_w = 40

    running = True
    while running:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / (1000 / 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "crash"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                    dino.jump()
                    started = True
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    dino.duck(True)
                if event.key == pygame.K_r and game_over:
                    dino = Dino()
                    obstacles = [spawn_cactus(GAME_SCREEN_W + 60, speed)]
                    clouds = [Cloud(GAME_SCREEN_W + i * 150, 30 + i * 20, 0.2 + i * 0.05) for i in range(3)]
                    total_score += score
                    score = 0
                    speed = base_speed
                    game_over = False
                    started = False
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    total_score += score
                    pygame.event.clear()
                    return int(total_score/50)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    dino.duck(False)

        speed = base_speed + (score // SPEED_INCREASE_EVERY) * 0.8
        dino.update()

        if not game_over:
            ground_offset = (ground_offset - speed) % (dash_w * 2)
            for c in clouds:
                c.update(dt * 0.6)
            if len(clouds) < 4 and random.random() < 0.01:
                clouds.append(Cloud(GAME_SCREEN_W + random.randint(20, 200),
                                    random.randint(30, 120),
                                    0.2 + random.random() * 0.3))
            for ob in list(obstacles):
                ob.speed = speed
                ob.update(dt)
                if ob.x + ob.width < -50:
                    obstacles.remove(ob)

            if obstacles:
                last = obstacles[-1]
                if last.x < GAME_SCREEN_W - random.randint(200, 380):
                    if random.random() < 0.2:
                        obstacles.append(spawn_ptero(GAME_SCREEN_W + random.randint(40, 100), speed))
                    else:
                        obstacles.append(spawn_cactus(GAME_SCREEN_W + random.randint(40, 100), speed))
            else:
                obstacles.append(spawn_cactus(GAME_SCREEN_W + 60, speed))

        if started and not game_over:
            score += int(0.1 * dt_ms)
            score += int(speed * 0.002 * dt_ms)

        drect = dino.rect()
        if not game_over:
            for ob in obstacles:
                if drect.colliderect(ob.rect()):
                    dino.dead = True
                    game_over = True
                    if score > high_score:
                        high_score = score
                    break

        # ----- DRAW -----
        screen.blit(BG_IMG, (0, 0))  # background first

        # clear game surface
        game_surface.fill((245, 245, 245))

        # clouds
        for c in clouds:
            c.draw(game_surface)

        # ground
        pygame.draw.line(game_surface, (83, 83, 83), (0, GROUND_Y), (GAME_SCREEN_W, GROUND_Y), 2)
        x = ground_offset
        while x < GAME_SCREEN_W:
            pygame.draw.rect(game_surface, (200, 200, 200), (int(x), GROUND_Y - 4, dash_w, 4))
            x += dash_w * 2

        # obstacles
        for ob in obstacles:
            ob.draw(game_surface)

        # dino
        dino.draw(game_surface)

        # score
        score_surf = font.render(f"SCORE: {score}", True, (30, 30, 30))
        hs_surf = font.render(f"HIGH: {high_score}", True, (100, 100, 100))
        game_surface.blit(score_surf, (GAME_SCREEN_W - 150, 10))
        game_surface.blit(hs_surf, (GAME_SCREEN_W - 150, 30))

        if not started:
            hint = font.render("Press SPACE or W to Jump. Press S to duck.", True, (120, 120, 120))
            game_surface.blit(hint, (GAME_SCREEN_W // 2 - hint.get_width() // 2, GAME_SCREEN_H // 2 - 10))
        if game_over:
            over = font.render("GAME OVER - Press R to restart or ESC to return", True, (160, 20, 20))
            game_surface.blit(over, (GAME_SCREEN_W // 2 - over.get_width() // 2, GAME_SCREEN_H // 2 - 10))

        # blit game surface on top of background at screen rect
        screen.blit(game_surface, (GAME_SCREEN_X, GAME_SCREEN_Y))

        if own_screen:
            pygame.display.flip()
        else:
            pygame.display.update()

    if own_screen:
        pygame.quit()
    return False


if __name__ == "__main__":
    run_trex(None)
