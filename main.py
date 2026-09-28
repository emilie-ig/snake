import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
CELL_SIZE = 25
GRID_SIZE = SCREEN_WIDTH // CELL_SIZE
FPS = 10

SNAKE_HEAD_COLOR = (1, 252, 128)
SNAKE_TAIL_COLOR = (0, 140, 80)
TONGUE_COLOR = (230, 30, 60)
BACKGROUND_COLOR = (104, 56, 0)
APPLE_COLOR = (250, 12, 4)
BORDER_COLOR = (232, 168, 0)
SCORE_COLOR = (248, 252, 248)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE")

font = pygame.font.Font(None, 36)

def lerp_color(c1, c2, t):
    """Mélange deux couleurs. t=0 donne c1, t=1 donne c2."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


class Snake:
    def __init__(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.grow = False

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

    def draw(self, surface):
        n = len(self.positions)
        pad = max(1, CELL_SIZE // 10) # petit espace autour de chaque segment
        radius = CELL_SIZE // 3 # arrondi des segments
        inner = CELL_SIZE - 2 * pad
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

        self.draw_head_details(surface)

    def draw_tongue(self, surface):
        # La langue sort 350 ms toutes les 1,5 s
        if pygame.time.get_ticks() % 1500 > 350:
            return
 
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        cx = head_x * CELL_SIZE + CELL_SIZE / 2
        cy = head_y * CELL_SIZE + CELL_SIZE / 2
        head_radius = CELL_SIZE
 
        start = (cx + dx * head_radius * 0.6, cy + dy * head_radius * 0.6)
        tip = (cx + dx * (head_radius + CELL_SIZE * 0.5),
               cy + dy * (head_radius + CELL_SIZE * 0.5))
        width =3 
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

        # La zone jouable fait (GRID_SIZE - 2) cases de côté
        if len(snake.positions) == (GRID_SIZE - 2) * (GRID_SIZE - 2):
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