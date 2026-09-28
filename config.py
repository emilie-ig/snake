import pygame

pygame.init()
pygame.mixer.init()

# Dimensions et paramètres
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
CELL_SIZE = 25
GRID_SIZE = SCREEN_WIDTH // CELL_SIZE
FPS = 10

SNAKE_HEAD_COLOR = (1, 252, 128)
SNAKE_TAIL_COLOR = (0, 140, 80)
TONGUE_COLOR = (230, 30, 60)
BACKGROUND_COLOR = (92, 48, 20)
BACKGROUND_COLOR_2 = (100, 54, 22)
APPLE_COLOR = (250, 12, 4)
BORDER_COLOR = (0, 140, 80)
SCORE_COLOR = (248, 252, 248)

TONGUE_PERIOD = 3500 # temps entre deux cycles (ms)
TONGUE_DELAY = 1000 # silence au début du son (ms)
TONGUE_DURATION = 500 # durée de la langue sortie (ms)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE")

font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 42)
small_font = pygame.font.Font(None, 28)

apple_sound = pygame.mixer.Sound("assets/sounds/apple_bite.mp3")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.mp3")
sss_sound = pygame.mixer.Sound("assets/sounds/ssss.mp3")
victory_sound = pygame.mixer.Sound("assets/sounds/victory.mp3")
boing_sound = pygame.mixer.Sound("assets/sounds/boingg.mp3")


def lerp_color(c1, c2, t):
    """Mélange deux couleurs. t=0 donne c1, t=1 donne c2."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))