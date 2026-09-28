import pygame
import random
import math
from config import CELL_SIZE, APPLE_COLOR

particles = []  # chaque éclat : [x, y, vx, vy, vie]

def spawn_particles(cell):
    cx = cell[0] * CELL_SIZE + CELL_SIZE // 2
    cy = cell[1] * CELL_SIZE + CELL_SIZE // 2
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        particles.append([cx, cy, math.cos(angle) * speed, math.sin(angle) * speed, 8])

def draw_particles(surface):
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        pygame.draw.circle(surface, APPLE_COLOR, (int(p[0]), int(p[1])), max(1, p[4] // 2))
    particles[:] = [p for p in particles if p[4] > 0]