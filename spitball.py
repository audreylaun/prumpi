import pygame
import math
import sys
from happiness import draw_happiness_meter, happiness_minigame

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Saloon Spitball")
clock = pygame.time.Clock()

#Images
background = pygame.image.load("data/image/spitball_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

volume_on_img = pygame.image.load("data/image/volume_on.png")
volume_off_img = pygame.image.load("data/image/volume_off.png")
volume_on_img = pygame.transform.scale(volume_on_img, (60, 60))
volume_off_img = pygame.transform.scale(volume_off_img, (60, 60))

coin_img = pygame.image.load("data/image/coin.png")
coin_img = pygame.transform.scale(coin_img, (80, 80))

font = pygame.font.SysFont("comic_sansms", 32)
button_color = (255, 225, 125)
button_text_color = (24, 100, 24)

coin_button_home = pygame.Rect(35, 600, 60, 60)

button_volume = pygame.Rect(930, 630, 60, 60)

def draw_volume(volume_on):
    if volume_on == True:
        screen.blit(volume_on_img, (button_volume.x, button_volume.y))
    elif volume_on == False:
        screen.blit(volume_off_img, (button_volume.x, button_volume.y))

# Colors
WHITE = (245, 245, 245)
BROWN = (139, 69, 19)
BLACK = (10, 10, 10)
GREEN = (50, 180, 50)
GRAY = (170, 170, 170)
BLUE = (120, 160, 255)

# Straw (comes up from bottom)
straw_x, straw_y = WIDTH // 2, HEIGHT
straw_length = 140          # longer straw
angle = -90.0
min_angle, max_angle = -160.0, -20.0
angle_speed_deg = 140.0  # deg/sec

# Spitball physics (use seconds for dt)
spitballs = []  # each is dict: {'x','y','vx','vy','t'}
shot_cooldown = 0.20  # seconds
last_shot = -10.0
spit_speed = 700.0    # pixels/second
spit_lifetime = 6.0   # seconds
air_drag = 0.6        # damping coefficient (per second)

# Bottle target
bottle = pygame.Rect(450, 140, 60, 100)

# Fan parameters (physical)
fan_rect = pygame.Rect(180, 230, 100, 100)
fan_base_angle = 0.0
fan_amp_deg = 40.0
fan_freq = 0.15   # slower oscillation (was 0.4)
fan_range = 420.0               # effective radius in pixels
cone_half_deg = 40.0            # half-angle of the wind cone
wind_accel_max = 1200.0         # max acceleration (px/s^2) at close range & center of cone

# Fan visuals
blade_spin = 0.0                # blade rotation offset (deg)
blade_spin_speed = 900.0        # deg/sec
num_blades = 3

def clamp(v, a, b):
    return max(a, min(b, v))

def draw_straw(surface, x, y, ang):
    rad = math.radians(ang)
    ex = x + math.cos(rad) * straw_length
    ey = y + math.sin(rad) * straw_length
    pygame.draw.line(surface, GRAY, (x, y), (ex, ey), 16)
    # pygame.draw.circle(surface, GRAY, (int(ex), int(ey)), 8)
    return ex, ey

def spawn_spit(x, y, ang, now):
    rad = math.radians(ang)
    vx = math.cos(rad) * spit_speed
    vy = math.sin(rad) * spit_speed
    spitballs.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 't': now})

def draw_rotating_fan(surface, rect, fan_dir_deg, blade_offset_deg):
    cx, cy = rect.center
    # base
    pygame.draw.line(surface, GRAY, (230, 325), (230,700), 8)
    pygame.draw.rect(surface, GRAY, rect, border_radius=8)
    # hub
    pygame.draw.circle(surface, WHITE, (cx, cy), 10)
    blade_len = rect.width * 0.45
    for i in range(num_blades):
        ang = math.radians(fan_dir_deg + blade_offset_deg + i * (360.0 / num_blades))
        ex = cx + math.cos(ang) * blade_len
        ey = cy + math.sin(ang) * blade_len
        pygame.draw.line(surface, BLACK, (cx, cy), (ex, ey), 8)

def apply_wind_to_ball(ball, fan_cx, fan_cy, fan_dir_vec, cone_cos, now):
    # Vector from fan to ball
    dx = ball['x'] - fan_cx
    dy = ball['y'] - fan_cy
    dist = math.hypot(dx, dy)
    if dist < 1e-5 or dist > fan_range:
        return  # too far or at center
    nx, ny = dx / dist, dy / dist
    dot = nx * fan_dir_vec[0] + ny * fan_dir_vec[1]  # cos of angle between them
    if dot <= cone_cos:
        return  # outside cone
    # attenuation by distance (linear falloff) and by how close to axis (dot)
    range_att = (1.0 - (dist / fan_range))  # 1 at center, 0 at edge
    axis_att = dot  # 1 when directly in front, smaller when off-axis
    accel = wind_accel_max * range_att * axis_att
    # acceleration vector is in fan_dir_vec (wind blows outward from fan)
    ax = fan_dir_vec[0] * accel
    ay = fan_dir_vec[1] * accel
    # apply acceleration per frame will be done externally with dt
    ball['ax'] += ax
    ball['ay'] += ay

def draw_wind_cone(surface, fan_cx, fan_cy, dir_deg, cone_half, rng):
    # visual helper: draw semi-transparent cone (not necessary; toggle on for debugging)
    points = []
    steps = 18
    start_ang = dir_deg - cone_half
    for i in range(steps + 1):
        a = math.radians(start_ang + (i / steps) * (2 * cone_half))
        points.append((fan_cx + math.cos(a) * rng, fan_cy + math.sin(a) * rng))
    points.insert(0, (fan_cx, fan_cy))
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(s, (120, 180, 255, 36), points)
    surface.blit(s, (0, 0))

def spitball_game(num_coins, happiness, HAPPINESS_MAX, volume_on):
    global angle, blade_spin, last_shot
    button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        dt = clock.tick(60) / 1000.0
        now = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # shoot from straw tip
                    if now - last_shot >= shot_cooldown:
                        tip_x, tip_y = draw_straw(screen, straw_x, straw_y, angle)  # for initial pos
                        spawn_spit(tip_x, tip_y, angle, now)
                        last_shot = now
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_home.collidepoint(mouse_pos):
                    return num_coins, happiness, volume_on
                if button_volume.collidepoint(mouse_pos):
                    if volume_on == True:
                        pygame.mixer.music.set_volume(0)
                        volume_on = False
                    elif volume_on == False:
                        pygame.mixer.music.set_volume(0.5)
                        volume_on = True

        keys = pygame.key.get_pressed()
        # WASD controls for angle (W/S up-down, A/D left-right — both change angle)
        if keys[pygame.K_w]:
            angle -= angle_speed_deg * dt
        if keys[pygame.K_s]:
            angle += angle_speed_deg * dt
        if keys[pygame.K_a]:
            angle -= angle_speed_deg * dt
        if keys[pygame.K_d]:
            angle += angle_speed_deg * dt

        angle = clamp(angle, min_angle, max_angle)

        # Update fan orientation (oscillating) and blade spin
        fan_dir = fan_base_angle + fan_amp_deg * math.sin(2.0 * math.pi * fan_freq * now)
        blade_spin = (blade_spin + blade_spin_speed * dt) % 360.0

        # Fan direction unit vector
        fan_rad = math.radians(fan_dir)
        fan_dir_vec = (math.cos(fan_rad), math.sin(fan_rad))
        cone_cos = math.cos(math.radians(cone_half_deg))

        # --- physics & drawing ---
        screen.blit(background, (0, 0))

        # (Optional) draw wind cone lightly for debugging/visual — comment out if you want invisible wind:
        draw_wind_cone(screen, fan_rect.centerx, fan_rect.centery, fan_dir, cone_half_deg, fan_range)

        draw_happiness_meter(screen, happiness, HAPPINESS_MAX)

        # Straw (drawn from bottom)
        tip_x, tip_y = draw_straw(screen, straw_x, straw_y, angle)

        # Fan visuals
        draw_rotating_fan(screen, fan_rect, fan_dir, blade_spin)

        # Update spitballs: use per-frame acceleration accumulation
        for ball in spitballs[:]:
            # initialize acceleration accumulator
            ball.setdefault('ax', 0.0)
            ball.setdefault('ay', 0.0)

            # apply wind if in range & cone: this adds to 'ax','ay'
            apply_wind_to_ball(ball, fan_rect.centerx, fan_rect.centery, fan_dir_vec, cone_cos, now)

            # integrate acceleration to velocity: a * dt
            ball['vx'] += ball['ax'] * dt
            ball['vy'] += ball['ay'] * dt

            # simple aerodynamic drag (exponential style)
            drag_multiplier = math.exp(-air_drag * dt)
            ball['vx'] *= drag_multiplier
            ball['vy'] *= drag_multiplier

            # integrate velocity to position
            ball['x'] += ball['vx'] * dt
            ball['y'] += ball['vy'] * dt

            # draw spitball
            pygame.draw.circle(screen, WHITE, (int(ball['x']), int(ball['y'])), 5)

            # collisions
            if bottle.collidepoint(ball['x'], ball['y']):
                spitballs.remove(ball)
                happiness +=1
                print("HIT! (bottle)")

            # cleanup: lifetime or off-screen
            if now - ball['t'] > spit_lifetime or not ( -50 <= ball['x'] <= WIDTH + 50 and -50 <= ball['y'] <= HEIGHT + 50):
                if ball in spitballs:
                    spitballs.remove(ball)

        # HUD / controls text
        txt1 = font.render("Hit the Prumpi Juice with spitballs!", True, button_color)
        txt2 = font.render("Use WASD to move straw", True, button_color)
        txt3 = font.render("Use SPACE to shoot", True, button_color)
        screen.blit(txt1, (8, 8))
        screen.blit(txt2, (8, 50))
        screen.blit(txt3, (8, 92))

        screen.blit(coin_img, (coin_button_home.x, coin_button_home.y))
        screen.blit(button_text_coin, (coin_button_home.x + 100, coin_button_home.y + 20))

        button_rect_home = pygame.Rect(700, 30, 250, 60)
        button_text_home = font.render("Return to Bar", True, button_text_color)

        pygame.draw.rect(screen, button_color, button_rect_home, border_radius=12)
        screen.blit(button_text_home, (button_rect_home.x + 10, button_rect_home.y + 5))

        if happiness >= HAPPINESS_MAX:
            happiness = 0
            coins_added = happiness_minigame()
            num_coins += coins_added
            button_text_coin = font.render(str(num_coins) + " Prumpi Coins", True, (0, 0, 0))

        draw_volume(volume_on)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    spitball_game(5, 10, 30, True)
