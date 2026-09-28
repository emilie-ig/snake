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
GOLDEN_APPLE_COLOR = (255, 215, 0)
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
golden_sound = pygame.mixer.Sound("assets/sounds/golden.mp3")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.mp3")
sss_sound = pygame.mixer.Sound("assets/sounds/ssss.mp3")
victory_sound = pygame.mixer.Sound("assets/sounds/victory.mp3")
boing_sound = pygame.mixer.Sound("assets/sounds/boingg.mp3")


def lerp_color(c1, c2, t):
    """Mélange deux couleurs. t=0 donne c1, t=1 donne c2."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

# Dictionnaire de traduction
LANGUAGES = {
    "FR": {
        "title": "SNAKE GAME",
        "select_mode": "Choisissez votre mode de jeu :",
        "start_hint": "Appuie sur [ESPACE] pour jouer",
        "lang_indicator": "Langue : FR (Appuie sur L)",
        "modes": {
            "classic": {
                "title": "Traditionnel",
                "desc": "Le Snake classique. Mange des pommes rouges et survis !",
                "icon": "assets/icon_classic.png"
            },
            "golden": {
                "title": "Pomme Dorée",
                "desc": "Des pommes dorées apparaissent ! (+3 pts, temporaires)",
                "icon": "assets/icon_golden.png"
            },
            "ice_spicy": {
                "title": "Glace & Piment",
                "desc": "Pomme bleue (ralentit) et piment (accélère + x2 pts).",
                "icon": "assets/icon_element.png"
            },
            "walls": {
                "title": "Labyrinthe",
                "desc": "Des murs internes apparaissent sur le terrain.",
                "icon": "assets/icon_walls.png"
            },
            "custom": {
                "title": "Sur Mesure",
                "desc": "Coche toi-même les options et règles voulues !",
                "icon": "assets/icon_custom.png"
            }
        }
    },
    "EN": {
        "title": "SNAKE GAME",
        "select_mode": "Select your game mode:",
        "start_hint": "Press [SPACE] to start",
        "lang_indicator": "Language: EN (Press L)",
        "modes": {
            "classic": {
                "title": "Classic",
                "desc": "The original Snake. Eat red apples and survive!",
                "icon": "assets/icon_classic.png"
            },
            "golden": {
                "title": "Golden Apple",
                "desc": "Golden apples spawn! (+3 pts, limited time)",
                "icon": "assets/icon_golden.png"
            },
            "ice_spicy": {
                "title": "Ice & Chili",
                "desc": "Blue apple (slows down) and chili (speed boost + x2 pts).",
                "icon": "assets/icon_element.png"
            },
            "walls": {
                "title": "Maze",
                "desc": "Internal wall obstacles spawn in the arena.",
                "icon": "assets/icon_walls.png"
            },
            "custom": {
                "title": "Custom",
                "desc": "Toggle and combine options as you like!",
                "icon": "assets/icon_custom.png"
            }
        }
    }
}