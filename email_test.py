import pygame, random, time

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inbox Minigame on Computer")

# Load the computer background image
computer_bg = pygame.image.load("data/image/computer.png").convert()
computer_bg = pygame.transform.scale(computer_bg, (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("arial", 24)

# Colors
EMAIL_COLOR = (255, 255, 255)
READ_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
CHECKBOX_COLOR = (180, 180, 180)
GREEN = (50, 200, 50)

# Define monitor screen area (adjust these numbers!)
monitor_rect = pygame.Rect(275, 115, 450, 250)

# Inbox setup
emails = []
next_email_time = time.time() + random.randint(5, 10)

class Email:
    def __init__(self, subject):
        self.subject = subject
        self.read = False
        self.rect = None
        self.checkbox_rect = None

def add_email():
    subjects = [
        "Dinosaur plushie shipment arrived",
        "Weekly sales report",
        "Gift shop inventory update",
        "Special discount on mugs",
        "Meeting at 3PM"
    ]
    subject = random.choice(subjects)
    emails.insert(0, Email(subject))

def draw_inbox():
    # Draw computer first
    screen.blit(computer_bg, (0, 0))

    # Draw inbox only inside the monitor area
    inbox_surface = pygame.Surface(monitor_rect.size)
    inbox_surface.fill((156,219,218))  # pale background

    # Draw unread counter
    unread_count = sum(1 for e in emails if not e.read)
    counter_text = FONT.render(f"Dino Mail Unread Messages: {unread_count}", True, TEXT_COLOR)
    inbox_surface.blit(counter_text, (20, 10))

    # Draw emails
    y = 50
    for email in emails[:6]:  # fit 6 per screen
        color = READ_COLOR if email.read else EMAIL_COLOR
        email.rect = pygame.Rect(20, y, 520, 50)
        pygame.draw.rect(inbox_surface, color, email.rect, border_radius=8)

        # Checkbox
        email.checkbox_rect = pygame.Rect(25, y + 10, 30, 30)
        pygame.draw.rect(inbox_surface, CHECKBOX_COLOR, email.checkbox_rect, border_radius=5)
        if email.read:
            pygame.draw.line(inbox_surface, GREEN, (30, y+25), (45, y+35), 3)
            pygame.draw.line(inbox_surface, GREEN, (45, y+35), (60, y+15), 3)

        # Subject
        text = FONT.render(email.subject, True, TEXT_COLOR)
        inbox_surface.blit(text, (70, y + 12))

        y += 60

    # Blit inbox onto monitor
    screen.blit(inbox_surface, monitor_rect.topleft)

running = True
clock = pygame.time.Clock()

while running:
    now = time.time()
    if now >= next_email_time:
        add_email()
        next_email_time = now + random.randint(5, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Convert mouse coords to monitor coords
            if monitor_rect.collidepoint(pos):
                local_pos = (pos[0] - monitor_rect.x, pos[1] - monitor_rect.y)
                for email in emails:
                    if email.checkbox_rect and email.checkbox_rect.collidepoint(local_pos):
                        email.read = True

    draw_inbox()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
