import pygame
import random
import math
from config import CELL_SIZE, APPLE_COLOR, SCORE_PANEL_X, SCORE_PANEL_Y, SCORE_PANEL_WIDTH

POPUP_FONT = pygame.font.SysFont("arial", 42, bold=True)
POPUP_DURATION = 45 

particles = []  # chaque éclat : [x, y, vx, vy, vie, color]
score_popups = []  # chaque popup : [texte, couleur, décalage vertical, vie restante]

def spawn_particles(cell, color=APPLE_COLOR):
    cx = cell[0] * CELL_SIZE + CELL_SIZE // 2
    cy = cell[1] * CELL_SIZE + CELL_SIZE // 2
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        particles.append([cx, cy, math.cos(angle) * speed, math.sin(angle) * speed, 8, color])

def draw_particles(surface):
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        color = p[5]
        pygame.draw.circle(surface, color, (int(p[0]), int(p[1])), max(1, p[4] // 2))
    particles[:] = [p for p in particles if p[4] > 0]

def spawn_score_popup(text, color):
    score_popups.append([text, color, 0, POPUP_DURATION])


def draw_score_popups(surface):
    for popup in score_popups:
        text, color, y_offset, life = popup
        progress = 1 - (life / POPUP_DURATION)
        popup[2] = -35 * progress  # monte de 35 px pendant l'animation
        popup[3] -= 1

        alpha = max(0, int(255 * (life / POPUP_DURATION)))

        # Le texte, rendu une fois pour connaître sa taille
        rendered = POPUP_FONT.render(text, True, color)
        padding_x, padding_y = 14, 8
        box_w = rendered.get_width() + padding_x * 2
        box_h = rendered.get_height() + padding_y * 2

        cx = SCORE_PANEL_X + SCORE_PANEL_WIDTH - 10  # collé au bord droit du panneau
        cy = SCORE_PANEL_Y + 92 + int(popup[2])  # aligné sur la hauteur du chiffre de score

        # Badge : fond sombre + bordure de la couleur de la pomme
        badge = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg_alpha = int(alpha * 0.85)
        pygame.draw.rect(badge, (20, 15, 12, bg_alpha), (0, 0, box_w, box_h), border_radius=10)
        pygame.draw.rect(badge, (*color, alpha), (0, 0, box_w, box_h), width=2, border_radius=10)

        rendered.set_alpha(alpha)
        badge.blit(rendered, (padding_x, padding_y))

        rect = badge.get_rect(midright=(cx, cy))
        surface.blit(badge, rect)

    score_popups[:] = [p for p in score_popups if p[3] > 0]