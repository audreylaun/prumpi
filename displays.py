import pygame

def announcement(screen, background, text_1, text_2, text_3):
    prumpi_head = pygame.image.load("data/image/prumpi_work.png")
    prumpi_head = pygame.transform.scale(prumpi_head, (400,400))

    speech_right = pygame.image.load("data/image/speech_bubble_right.png")
    speech_right = pygame.transform.scale(speech_right, (500,100))

    welcome_bubble = pygame.transform.scale(speech_right, (500, 300))
    welcome_prumpi_pos = (100, 300)
    welcome_bubble_pos = (400, 200)

    font = pygame.font.SysFont("comic_sansms", 32)

    screen.blit(background, (0, 0))
    screen.blit(prumpi_head, welcome_prumpi_pos)
    screen.blit(welcome_bubble, welcome_bubble_pos)
    complete_text_1 = font.render(text_1, True, (0, 0, 0))
    complete_text_2 = font.render(text_2, True, (0, 0, 0))
    complete_text_3 = font.render(text_3, True, (0, 0, 0))

    screen.blit(complete_text_1, (welcome_bubble_pos[0] + 30, welcome_bubble_pos[1] + 40))
    screen.blit(complete_text_2, (welcome_bubble_pos[0] + 30, welcome_bubble_pos[1] + 80))
    screen.blit(complete_text_3, (welcome_bubble_pos[0] + 30, welcome_bubble_pos[1] + 120))