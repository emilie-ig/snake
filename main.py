import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
CELL_SIZE = 25
GRID_SIZE = SCREEN_WIDTH // CELL_SIZE
FPS = 10

SNAKE_COLOR = (1, 252, 128)
BACKGROUND_COLOR = (104, 56, 0)
APPLE_COLOR = (250, 12, 4)
BORDER_COLOR = (232, 168, 0)
SCORE_COLOR = (248, 252, 248)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE")

font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(5,5), (4,5), (3,5)]
        self.direction = (1,0)
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if(new_head in self.positions or 
           not (1<= new_head[0] < GRID_SIZE - 1 and 1<= new_head[1 < GRID_SIZE -1])):
            return False

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop() #n'a pas mangé de pomme, donc on supprime pas la queue
        else:
            self.grow = False

        return True

    def change_direction(self, direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if direction != opposite_direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for x,y in self.positions:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

        head_x, head_y = self.positions[0]

        # Position de base de la tête en pixels
        head_pixel_x = head_x * CELL_SIZE
        head_pixel_y = head_y * CELL_SIZE

        # Position des yeux selon la direction
        if self.direction == (1, 0):  # droite
            eye1 = pygame.Rect(head_pixel_x + 15, head_pixel_y + 5, 5, 5)
            eye2 = pygame.Rect(head_pixel_x + 15, head_pixel_y + 15, 5, 5)

        elif self.direction == (-1, 0):  # gauche
            eye1 = pygame.Rect(head_pixel_x + 5, head_pixel_y + 5, 5, 5)
            eye2 = pygame.Rect(head_pixel_x + 5, head_pixel_y + 15, 5, 5)

        elif self.direction == (0, -1):  # haut
            eye1 = pygame.Rect(head_pixel_x + 5, head_pixel_y + 5, 5, 5)
            eye2 = pygame.Rect(head_pixel_x + 15, head_pixel_y + 5, 5, 5)

        else:  # bas
            eye1 = pygame.Rect(head_pixel_x + 5, head_pixel_y + 15, 5, 5)
            eye2 = pygame.Rect(head_pixel_x + 15, head_pixel_y + 15, 5, 5)

        pygame.draw.rect(surface, (0, 0, 0), eye1)
        pygame.draw.rect(surface, (0, 0, 0), eye2)


class Apple:
    def __init__(self, snake):
        self.positions = self.random_position(snake)

    def random_position(self, snake):
        while True:
            position = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
            if position not in snake.positions:
                return position

    def draw(self, surface):
        rect = pygame.Rect(self.positions[0] * CELL_SIZE, self.positions[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, APPLE_COLOR, rect)

        
def draw_background(surface):
    surface.fill(BACKGROUND_COLOR)

def draw_border(surface):
    pygame.draw.rect(surface, BORDER_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), CELL_SIZE)

def display_score(surface, score):
    text = font.render(f"Score: {score}", True, SCORE_COLOR)
    surface.blit(text, (10, 10))

def game_over_screen(surface, score):
    draw_background(surface)
    game_over_text = font.render("GAME OVER", True, SCORE_COLOR)
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    restart_text = font.render("Press Space to restart", True, SCORE_COLOR)
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT //4))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT //3))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT //2))

def victory_screen(surface, score):
    draw_background(surface)
    victory_text = font.render("YOU WIN", True, SCORE_COLOR)
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    restart_text = font.render("Press Space to restart", True, SCORE_COLOR)
    surface.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT //4))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT //3))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT //2))

def main():

    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple(snake)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        snake.change_direction((0, -1))
                    case pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    case pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    case pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                    case pygame.K_SPACE:
                        if not running:
                            main()

        if not snake.move():
            game_over_screen(screen, score)
            pygame.display.flip()
            running = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main()

        if snake.positions[0] == apple.positions:
            snake.grow_snake()
            apple = Apple(snake)
            score += 1

        draw_background(screen)
        draw_border(screen)
        snake.draw(screen)
        apple.draw(screen)
        display_score(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

        if len(snake.positions) == GRID_SIZE * GRID_SIZE:
            victory_screen(screen, score)
            pygame.display.flip()
            running = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main()

main()