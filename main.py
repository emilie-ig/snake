import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
CELL_SIZE = 25
GRID_SIZE = SCREEN_WIDTH // SCREEN_HEIGHT
FPS = 10

SNAKE_COLOR = (248, 168, 0)
BACKGROUND_COLOR = (104, 56, 0)
APPLE_COLOR = (1, 252, 128)
BORDER_COLOR = (232, 168, 0)
SCORE_COLOR = (248, 252, 248)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE")

font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(5,5), (4,5), ((3,5))]
        self.direction = (1,0)
        self.grow = False

    def move(self):
        head_x, head_y = self.position[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if(new_head in self.position or 
           not (1<= new_head[0] < GRID_SIZE - 1 and 1<= new_head[1 < GRID_SIZE -1])):
            return False

        self.positon.insert(0, new_head)

        if not self.grow:
            self.positions.pop() #n'a pas mangé de pomme, donc on supprime pas la queue
        else:
            self.grow = False

        return True

    def change_direction(self, direction):
        opposite_direction = (-self.direction[0, -self.direction[1]])
        if direction != opposite_direction:
            self.direction = direction

    def grow_snake(self, surface):
        for x,y in self.positions:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

        head_x, head_y = self.positions[0]
        eye1 = pygame.Rect (head_x * CELL_SIZE + 8, head_y + 8, 5, 5)
        eye2 = pygame.Rect (head_x * CELL_SIZE + 17, head_y + 8, 5, 5)
        pygame.drax.rect(surface, (0,0,0), eye1)
        pygame.drax.rect(surface, (0,0,0), eye2)


class Apple:
    def __init__(self, snake):
        self.position = self.random_position(snake)

    def random_position(self, snake):
        while True:
            position = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
            if position not in snake.positions:
                return position

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.Rect(surface, APPLE_COLOR, rect)

        
