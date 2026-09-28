import pygame
import math
from config import (
    GRID_SIZE, CELL_SIZE, SNAKE_HEAD_COLOR, SNAKE_TAIL_COLOR,
    TONGUE_COLOR, TONGUE_PERIOD, TONGUE_DELAY, TONGUE_DURATION,
    sss_sound, lerp_color
)


class Snake:
    def __init__(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.grow = False
        self.mouth_open = False

    def move(self):
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if (new_head in self.positions or
                not (1 <= new_head[0] < GRID_SIZE - 1 and 1 <= new_head[1] < GRID_SIZE - 1)):
            return False

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()  # n'a pas mangé de pomme, donc on supprime la queue
        else:
            self.grow = False

        return True

    def change_direction(self, direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if direction != opposite_direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True

    def draw(self, surface, stunned=False):
        n = len(self.positions)
        pad = max(1, CELL_SIZE // 10) # petit espace autour de chaque segment
        radius = CELL_SIZE // 3 # arrondi des segments
        inner = CELL_SIZE - 2 * pad
        if not stunned:
            self.draw_tongue(surface)

        # On dessine de la queue vers la tête pour que la tête soit au-dessus
        for i in range(n - 1, -1, -1):
            x, y = self.positions[i]
            t = i / max(n - 1, 1)
            color = lerp_color(SNAKE_HEAD_COLOR, SNAKE_TAIL_COLOR, t)
            dark = lerp_color(color, (0, 0, 0), 0.25)

            px, py = x * CELL_SIZE, y * CELL_SIZE

            # Segment arrondi (la tête est un peu plus grosse)
            if i == 0:
                rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE).inflate(1, 1)
                pygame.draw.rect(surface, color, rect, border_radius=rect.width // 2 - 2)
            else:
                rect = pygame.Rect(px + pad, py + pad, inner, inner)
                pygame.draw.rect(surface, color, rect, border_radius=radius)

                # Raccord avec le segment précédent (côté tête) pour un corps continu
                nx, ny = self.positions[i - 1]
                if nx != x:  # voisin horizontal
                    left = min(x, nx) * CELL_SIZE + CELL_SIZE // 2
                    connector = pygame.Rect(left, py + pad, CELL_SIZE, inner)
                else:        # voisin vertical
                    top = min(y, ny) * CELL_SIZE + CELL_SIZE // 2
                    connector = pygame.Rect(px + pad, top, inner, CELL_SIZE)
                pygame.draw.rect(surface, color, connector)

        if stunned:
            self.draw_stunned_head(surface)
        else:
            self.draw_head_details(surface)

    def draw_tongue(self, surface):
        t = pygame.time.get_ticks() % TONGUE_PERIOD

        if self.mouth_open:
            sss_sound.stop()  # pas de sifflement bouche ouverte
        elif t < getattr(self, "last_t", TONGUE_PERIOD):
            # on lance le son (la 1re seconde est muette)
            sss_sound.play(maxtime=TONGUE_DELAY + TONGUE_DURATION)
        self.last_t = t

        # Pas de langue si la bouche est ouverte, ou si ce n'est pas son moment
        if self.mouth_open or not (TONGUE_DELAY <= t <= TONGUE_DELAY + TONGUE_DURATION):
            return

        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        cx = head_x * CELL_SIZE + CELL_SIZE / 2
        cy = head_y * CELL_SIZE + CELL_SIZE / 2
        head_radius = CELL_SIZE

        start = (cx + dx * head_radius * 0.6, cy + dy * head_radius * 0.6)
        tip = (cx + dx * (head_radius + CELL_SIZE * 0.5),
            cy + dy * (head_radius + CELL_SIZE * 0.5))
        width = 3
        pygame.draw.line(surface, TONGUE_COLOR, start, tip, width)

        # Bout fourchu (-dy, dx) est perpendiculaire à la direction
        fork = CELL_SIZE * 0.2
        for sign in (-1, 1):
            end = (tip[0] + dx * fork + (-dy) * fork * sign,
                tip[1] + dy * fork + dx * fork * sign)
            pygame.draw.line(surface, TONGUE_COLOR, tip, end, width)

    def draw_head_details(self, surface):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        cx = head_x * CELL_SIZE + CELL_SIZE / 2
        cy = head_y * CELL_SIZE + CELL_SIZE / 2

        if self.mouth_open:
            # Bajoues : deux joues rondes sur les côtés de la tête
            for sign in (-1, 1):
                jx = cx + dx * CELL_SIZE * 0.12 + (-dy) * CELL_SIZE * 0.38 * sign
                jy = cy + dy * CELL_SIZE * 0.12 + dx * CELL_SIZE * 0.38 * sign
                pygame.draw.circle(surface, SNAKE_HEAD_COLOR, (int(jx), int(jy)), int(CELL_SIZE * 0.32))

            # Museau : quelques pixels de plus devant, au niveau de la bouche
            mux = int(cx + dx * CELL_SIZE * 0.3)
            muy = int(cy + dy * CELL_SIZE * 0.3)
            pygame.draw.circle(surface, SNAKE_HEAD_COLOR, (mux, muy), int(CELL_SIZE * 0.45))
                
            # Bouche
            mx = cx + dx * CELL_SIZE * 0.5
            my = cy + dy * CELL_SIZE * 0.5
            long_side = int(CELL_SIZE * 0.5)    # largeur de la bouche
            short_side = int(CELL_SIZE * 0.26)  # ouverture
            w, h = (short_side, long_side) if dx != 0 else (long_side, short_side)
            mouth = pygame.Rect(0, 0, w, h)
            mouth.center = (int(mx), int(my))
            pygame.draw.ellipse(surface, (120, 0, 20), mouth)

        forward = CELL_SIZE * 0.15 # décalage des yeux vers l'avant
        side = CELL_SIZE * 0.24 # écart entre les deux yeux
        eye_radius = max(3, int(CELL_SIZE * 0.17))
        pupil_radius = max(2, int(CELL_SIZE * 0.09))

        # (-dy, dx) est le vecteur perpendiculaire à la direction
        for sign in (-1, 1):
            ex = cx + dx * forward + (-dy) * side * sign
            ey = cy + dy * forward + dx * side * sign
            pygame.draw.circle(surface, (255, 255, 255), (int(ex), int(ey)), eye_radius)
            # La pupille regarde dans la direction du serpent
            pupil = (int(ex + dx * 2), int(ey + dy * 2))
            pygame.draw.circle(surface, (0, 0, 0), pupil, pupil_radius)

    def draw_stunned_head(self, surface):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        cx = head_x * CELL_SIZE + CELL_SIZE / 2
        cy = head_y * CELL_SIZE + CELL_SIZE / 2

        forward = CELL_SIZE * 0.15
        side = CELL_SIZE * 0.24
        r = 3

        # Yeux en croix
        for sign in (-1, 1):
            ex = cx + dx * forward + (-dy) * side * sign
            ey = cy + dy * forward + dx * side * sign
            pygame.draw.line(surface, (0, 0, 0), (ex - r, ey - r), (ex + r, ey + r), 2)
            pygame.draw.line(surface, (0, 0, 0), (ex - r, ey + r), (ex + r, ey - r), 2)

        # Trois étoiles qui tournent au-dessus de la tête
        now = pygame.time.get_ticks()
        for k in range(3):
            angle = now / 150 + k * 2 * math.pi / 3
            sx = cx + math.cos(angle) * CELL_SIZE * 0.7
            sy = cy - CELL_SIZE * 0.9 + math.sin(angle) * CELL_SIZE * 0.25
            pygame.draw.circle(surface, (255, 230, 0), (int(sx), int(sy)), 4)