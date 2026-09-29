import pygame
import sys
import os
from config import (
    CELL_SIZE, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    SCORE_COLOR, BORDER_COLOR, APPLE_COLOR, GOLDEN_APPLE_COLOR, ICE_APPLE_COLOR, CHILI_APPLE_COLOR
)
from snake import Snake
from apple import Apple, GoldenApple, IceApple, ChiliApple
from ui import draw_background as draw_checkered_background, draw_border
from main import draw_walls

PALETTE_WIDTH = 210
OUTPUT_DIR = "assets/thumbnails"
os.makedirs(OUTPUT_DIR, exist_ok=True)

screen = pygame.display.set_mode((SCREEN_WIDTH + PALETTE_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Éditeur de vignettes")

ui_font = pygame.font.Font(None, 22)
hint_font = pygame.font.Font(None, 18)
small_font = pygame.font.Font(None, 20)

TOOLS = [
    ("apple", "Pomme rouge", APPLE_COLOR),
    ("golden", "Pomme dorée", GOLDEN_APPLE_COLOR),
    ("ice_apple", "Pomme glace", ICE_APPLE_COLOR),
    ("chili_apple", "Pomme piment", CHILI_APPLE_COLOR),
    ("wall", "Mur", (80, 80, 90)),
    ("snake_normal", "Serpent normal", (1, 252, 128)),
    ("snake_chili", "Serpent piment", (255, 60, 20)),
    ("snake_ice", "Serpent glace", (150, 220, 255)),
    ("eraser", "Gomme", (200, 200, 200)),
]
APPLE_CLASSES = {"apple": Apple, "golden": GoldenApple, "ice_apple": IceApple, "chili_apple": ChiliApple}

# Fonds disponibles : None = quadrillage d'origine, sinon une couleur unie
BG_OPTIONS = [
    ("Quadrillé", None),
    ("Marron", (92, 48, 20)),
    ("Sombre", (25, 25, 30)),
    ("Blanc", (240, 240, 240)),
    ("Vert nuit", (15, 40, 25)),
    ("Noir", (0, 0, 0)),
]

current_tool = "apple"
current_scale = 1.0   # taille des pommes posées, ajustée avec +/-
bg_index = 0           # index dans BG_OPTIONS

walls = set()
apples = []  # liste de dicts : {"cls":, "pos":, "scale":}

# Un serpent = {"path": [...], "direction": (1,0), "state": "normal", "mouth_open": False}
snakes = []              # serpents déjà validés
current_snake = {"path": [], "direction": (1, 0), "state": "normal", "mouth_open": False}


def make_apple_instance(cls, pos):
    """Crée une pomme affichable directement à une position choisie, sans tirage aléatoire."""
    obj = cls.__new__(cls)
    obj.positions = pos
    if cls is GoldenApple:
        obj.spawn_time = pygame.time.get_ticks()
        obj.duration = 999999
    return obj


def draw_scaled_apple(surface, cls, pos, scale):
    """Dessine une pomme à une taille différente de CELL_SIZE, sans modifier apple.py."""
    temp = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    apple = make_apple_instance(cls, (0, 0))
    apple.draw(temp)

    size = max(4, int(CELL_SIZE * scale))
    scaled = pygame.transform.smoothscale(temp, (size, size))

    cx = pos[0] * CELL_SIZE + CELL_SIZE // 2
    cy = pos[1] * CELL_SIZE + CELL_SIZE // 2
    rect = scaled.get_rect(center=(cx, cy))
    surface.blit(scaled, rect)


def cell_from_mouse(pos):
    mx, my = pos
    if mx >= SCREEN_WIDTH:
        return None
    cx, cy = mx // CELL_SIZE, my // CELL_SIZE
    if 1 <= cx <= GRID_SIZE - 2 and 1 <= cy <= GRID_SIZE - 2:
        return (cx, cy)
    return None


def handle_left_click(cell):
    global apples, walls

    if current_tool == "wall":
        walls.symmetric_difference_update({cell})

    elif current_tool == "eraser":
        walls.discard(cell)
        apples[:] = [a for a in apples if a["pos"] != cell]
        current_snake["path"][:] = [p for p in current_snake["path"] if p != cell]
        for s in snakes:
            s["path"][:] = [p for p in s["path"] if p != cell]

    elif current_tool.startswith("snake_"):
        current_snake["state"] = current_tool.replace("snake_", "")
        if not current_snake["path"] or current_snake["path"][-1] != cell:
            current_snake["path"].append(cell)

    else:  # une des pommes
        cls = APPLE_CLASSES[current_tool]
        existing = [a for a in apples if a["pos"] == cell]
        if existing:
            apples[:] = [a for a in apples if a["pos"] != cell]
        else:
            apples.append({"cls": cls, "pos": cell, "scale": current_scale})


def handle_right_click(cell):
    walls.discard(cell)
    apples[:] = [a for a in apples if a["pos"] != cell]
    current_snake["path"][:] = [p for p in current_snake["path"] if p != cell]
    for s in snakes:
        s["path"][:] = [p for p in s["path"] if p != cell]


def new_snake():
    """Valide le serpent en cours (s'il a au moins une case) et en commence un nouveau."""
    global current_snake
    if current_snake["path"]:
        snakes.append(current_snake)
    current_snake = {"path": [], "direction": (1, 0), "state": "normal", "mouth_open": False}


def draw_palette():
    panel = pygame.Rect(SCREEN_WIDTH, 0, PALETTE_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, (30, 30, 35), panel)

    y = 12
    label = ui_font.render("Outils", True, (180, 180, 180))
    screen.blit(label, (SCREEN_WIDTH + 10, y))
    y += 24

    buttons = {}
    for key, name, color in TOOLS:
        rect = pygame.Rect(SCREEN_WIDTH + 10, y, PALETTE_WIDTH - 20, 32)
        buttons[key] = rect
        is_active = (key == current_tool)
        pygame.draw.rect(screen, (60, 60, 70) if not is_active else (90, 90, 40), rect, border_radius=6)
        pygame.draw.rect(screen, color, rect, 2, border_radius=6)
        text = small_font.render(name, True, SCORE_COLOR)
        screen.blit(text, (rect.x + 8, rect.y + 6))
        y += 38

    y += 8
    label = ui_font.render("Fond", True, (180, 180, 180))
    screen.blit(label, (SCREEN_WIDTH + 10, y))
    y += 24

    bg_buttons = {}
    swatch_size = 28
    per_row = 3
    start_x = SCREEN_WIDTH + 10
    for i, (name, color) in enumerate(BG_OPTIONS):
        row, col = divmod(i, per_row)
        rect = pygame.Rect(start_x + col * (swatch_size + 6), y + row * (swatch_size + 6), swatch_size, swatch_size)
        bg_buttons[i] = rect
        display_color = color if color else (110, 110, 110)
        pygame.draw.rect(screen, display_color, rect, border_radius=6)
        border_col = (255, 215, 0) if i == bg_index else (90, 90, 90)
        pygame.draw.rect(screen, border_col, rect, 2, border_radius=6)
        if color is None:  # petit motif pour représenter le quadrillage
            pygame.draw.line(screen, (150, 150, 150), rect.topleft, rect.bottomright, 1)
            pygame.draw.line(screen, (150, 150, 150), rect.topright, rect.bottomleft, 1)
    y += (len(BG_OPTIONS) // per_row + 1) * (swatch_size + 6) + 10

    scale_text = ui_font.render(f"Taille pomme : {current_scale:.1f}x", True, SCORE_COLOR)
    screen.blit(scale_text, (SCREEN_WIDTH + 10, y))
    y += 26

    nb_snakes = len(snakes) + (1 if current_snake["path"] else 0)
    snake_text = ui_font.render(f"Serpents : {nb_snakes}", True, SCORE_COLOR)
    screen.blit(snake_text, (SCREEN_WIDTH + 10, y))
    y += 30

    hints = [
        "Clic droit : effacer",
        "+/- : taille pommes",
        "N : nouveau serpent",
        "C : tout effacer",
        "Z : annuler segment",
        "M : bouche ouv./fermée",
        "Flèches : direction tête",
        "S : enregistrer l'image",
    ]
    for line in hints:
        text = hint_font.render(line, True, (170, 170, 170))
        screen.blit(text, (SCREEN_WIDTH + 10, y))
        y += 19

    return buttons, bg_buttons


def build_snake_object(snake_data):
    snake = Snake()
    snake.positions = snake_data["path"] if snake_data["path"] else [(-5, -5)]
    snake.direction = snake_data["direction"]
    snake.mouth_open = snake_data["mouth_open"]
    snake.boosted = (snake_data["state"] == "chili")
    snake.frozen = (snake_data["state"] == "ice")
    return snake


def draw_scene_background(surface):
    _, color = BG_OPTIONS[bg_index]
    if color is None:
        draw_checkered_background(surface)
    else:
        surface.fill(color, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


def save_screenshot():
    grid_surface = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    name = input("Nom du fichier (sans extension) : ").strip() or "vignette"
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    pygame.image.save(grid_surface, path)
    print(f"Enregistré : {path}")


def main():
    global current_tool, current_scale, bg_index

    clock = pygame.time.Clock()
    dragging_button = "left"
    tool_buttons = {}
    bg_buttons = {}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    walls.clear()
                    apples.clear()
                    snakes.clear()
                    current_snake["path"].clear()
                elif event.key == pygame.K_z and current_snake["path"]:
                    current_snake["path"].pop()
                elif event.key == pygame.K_m:
                    current_snake["mouth_open"] = not current_snake["mouth_open"]
                elif event.key == pygame.K_n:
                    new_snake()
                elif event.key == pygame.K_s:
                    save_screenshot()
                elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    current_scale = min(2.5, round(current_scale + 0.1, 1))
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    current_scale = max(0.4, round(current_scale - 0.1, 1))
                elif event.key == pygame.K_UP:
                    current_snake["direction"] = (0, -1)
                elif event.key == pygame.K_DOWN:
                    current_snake["direction"] = (0, 1)
                elif event.key == pygame.K_LEFT:
                    current_snake["direction"] = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_snake["direction"] = (1, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= SCREEN_WIDTH:
                    for key, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_tool = key
                    for idx, rect in bg_buttons.items():
                        if rect.collidepoint(event.pos):
                            bg_index = idx
                else:
                    cell = cell_from_mouse(event.pos)
                    if cell:
                        if event.button == 1:
                            dragging_button = "left"
                            handle_left_click(cell)
                        elif event.button == 3:
                            dragging_button = "right"
                            handle_right_click(cell)

            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if not current_tool.startswith("snake_"):
                    cell = cell_from_mouse(event.pos)
                    if cell and dragging_button == "left":
                        handle_left_click(cell)

        draw_scene_background(screen)
        draw_border(screen)
        draw_walls(screen, walls)

        for a in apples:
            draw_scaled_apple(screen, a["cls"], a["pos"], a["scale"])

        for s in snakes:
            build_snake_object(s).draw(screen)
        if current_snake["path"]:
            build_snake_object(current_snake).draw(screen)

        tool_buttons, bg_buttons = draw_palette()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()