import pygame
import random
from config import GRID_SIZE, CELL_SIZE, APPLE_COLOR, GOLDEN_APPLE_COLOR, CHILI_APPLE_COLOR, ICE_APPLE_COLOR, lerp_color


class Apple:
    def __init__(self, snake):
        self.positions = self.random_position(snake)

    def random_position(self, snake):
        while True:
            position = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
            if position not in snake.positions:
                return position

    def draw(self, surface):
        x = self.positions[0] * CELL_SIZE
        y = self.positions[1] * CELL_SIZE
        c = CELL_SIZE

        # Pomme : elle remplit presque toute la case
        center = (x + c // 2, y + c // 2 + c // 12)
        radius = c // 2 - 1
        pygame.draw.circle(surface, APPLE_COLOR, center, radius)

        # Ombre en bas à droite pour donner du volume
        shade = lerp_color(APPLE_COLOR, (0, 0, 0), 0.3)
        pygame.draw.circle(surface, shade, (center[0] + c // 10, center[1] + c // 10), radius // 2)
        pygame.draw.circle(surface, APPLE_COLOR, (center[0] - c // 40, center[1] - c // 40), radius - c // 8)

        # Reflet en haut à gauche
        shine = pygame.Rect(x + c // 4, y + c // 4, c // 5, c // 4)
        pygame.draw.ellipse(surface, (255, 200, 200), shine)

        # Tige
        stem_start = (x + c // 2, y + c // 4)
        stem_end = (x + c // 2 + c // 12, y + c // 20)
        pygame.draw.line(surface, (90, 50, 10), stem_start, stem_end, max(2, c // 12))

        # Feuille
        leaf = pygame.Rect(x + c // 2 + c // 12, y + c // 20, c // 3, c // 5)
        pygame.draw.ellipse(surface, (50, 180, 50), leaf)


class GoldenApple(Apple):
    def __init__(self, snake, duration_ms=5000):
        super().__init__(snake)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration_ms  # Temps avant de disparaître (en ms)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration

    def draw(self, surface):
        x = self.positions[0] * CELL_SIZE
        y = self.positions[1] * CELL_SIZE
        c = CELL_SIZE

        center = (x + c // 2, y + c // 2 + c // 12)
        radius = c // 2 - 1
        pygame.draw.circle(surface, GOLDEN_APPLE_COLOR, center, radius)

        # Ombre dorée plus sombre
        shade = lerp_color(GOLDEN_APPLE_COLOR, (0, 0, 0), 0.3)
        pygame.draw.circle(surface, shade, (center[0] + c // 10, center[1] + c // 10), radius // 2)
        pygame.draw.circle(surface, GOLDEN_APPLE_COLOR, (center[0] - c // 40, center[1] - c // 40), radius - c // 8)

        # Reflet étincelant (blanc)
        shine = pygame.Rect(x + c // 4, y + c // 4, c // 5, c // 4)
        pygame.draw.ellipse(surface, (255, 255, 255), shine)

        # Tige
        stem_start = (x + c // 2, y + c // 4)
        stem_end = (x + c // 2 + c // 12, y + c // 20)
        pygame.draw.line(surface, (90, 50, 10), stem_start, stem_end, max(2, c // 12))

        # Feuille
        leaf = pygame.Rect(x + c // 2 + c // 12, y + c // 20, c // 3, c // 5)
        pygame.draw.ellipse(surface, (50, 180, 50), leaf)

class IceApple(Apple):
    """Ralentit le serpent pendant quelques secondes."""
    def draw(self, surface):
        x = self.positions[0] * CELL_SIZE
        y = self.positions[1] * CELL_SIZE
        c = CELL_SIZE
        center = (x + c // 2, y + c // 2)
        pygame.draw.circle(surface, ICE_APPLE_COLOR, center, c // 2 - 1)
        shine = pygame.Rect(x + c // 4, y + c // 4, c // 5, c // 4)
        pygame.draw.ellipse(surface, (230, 245, 255), shine)


class ChiliApple(Apple):
    """Accélère le serpent et vaut plus de points."""
    def draw(self, surface):
        x = self.positions[0] * CELL_SIZE
        y = self.positions[1] * CELL_SIZE
        c = CELL_SIZE
        # Corps du piment : un triangle pointant vers le bas
        points = [(x + c * 0.2, y + c * 0.25), (x + c * 0.8, y + c * 0.25), (x + c * 0.5, y + c * 0.85)]
        pygame.draw.polygon(surface, CHILI_APPLE_COLOR, points)
        # Petite tige verte
        pygame.draw.line(surface, (50, 150, 50), (x + c * 0.5, y + c * 0.25), (x + c * 0.5, y + c * 0.1), 3)