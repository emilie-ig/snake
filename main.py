import pygame
import sys
import random
from config import (
    FPS, GRID_SIZE, CELL_SIZE, WALL_COLOR, screen,
    APPLE_COLOR, GOLDEN_APPLE_COLOR, ICE_APPLE_COLOR, CHILI_APPLE_COLOR, SPEED_EFFECT_DURATION,
    apple_sound, golden_sound, ice_sound, chili_sound, gameover_sound, victory_sound
)
from snake import Snake
from apple import Apple, GoldenApple, IceApple, ChiliApple
from fx import particles, spawn_particles, draw_particles
from ui import (
    draw_background, draw_border, display_score,
    game_over_screen, victory_screen, stun_animation, start_screen
)


def draw_pause_overlay(screen):
    """Dessine un voile gris semi-transparent et l'affichage PAUSE."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 160))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont("arial", 48, bold=True)
    text = font.render("PAUSE", True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, rect)


def run_countdown(screen, snake, apple, golden_apple, score):
    """Affiche un décompte 3, 2, 1 tout en conservant le fond de jeu."""
    font = pygame.font.SysFont("arial", 72, bold=True)
    clock = pygame.time.Clock()

    for count in range(3, 0, -1):
        start_ticks = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_ticks < 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Redessine l'état actuel du jeu en arrière-plan
            draw_background(screen)
            draw_border(screen)
            snake.draw(screen)
            apple.draw(screen)
            if golden_apple:
                golden_apple.draw(screen)
            draw_particles(screen)
            display_score(screen, score)

            # Voile léger pour la lisibilité
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))

            # Affichage du chiffre du décompte
            text = font.render(str(count), True, (255, 255, 255))
            rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, rect)

            pygame.display.flip()
            clock.tick(FPS)

def generate_walls(snake, count=15):
    walls = []
    while len(walls) < count:
        pos = (random.randint(2, GRID_SIZE - 3), random.randint(2, GRID_SIZE - 3))
        if pos not in snake.positions and pos not in walls:
            walls.append(pos)
    return walls


def draw_walls(surface, walls):
    for (x, y) in walls:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, WALL_COLOR, rect, border_radius=4)


def run_game(mode_key):
    particles.clear()
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple(snake)
    extra_apple = None # pomme dorée, glace ou piment, selon le mode
    walls = generate_walls(snake) if mode_key == "walls" else []
    speed_effect_end = 0
    score = 0

    direction_queue = []
    paused = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused:
                        run_countdown(screen, snake, apple, extra_apple, score)
                        paused = False
                    else:
                        paused = True
                elif not paused and len(direction_queue) < 2:
                    match event.key:
                        case pygame.K_UP:
                            direction_queue.append((0, -1))
                        case pygame.K_DOWN:
                            direction_queue.append((0, 1))
                        case pygame.K_LEFT:
                            direction_queue.append((-1, 0))
                        case pygame.K_RIGHT:
                            direction_queue.append((1, 0))
                        case pygame.K_SPACE:
                            if not running:
                                main()

        # Si le jeu est en pause, on affiche le voile et on fige l'état
        if paused:
            draw_pause_overlay(screen)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # On dépile UNE seule direction par frame
        if direction_queue:
            next_direction = direction_queue.pop(0)
            snake.change_direction(next_direction)

        if not snake.move():
            stun_animation(snake, apple, score)
            gameover_sound.play()
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

        # --- Pomme classique, toujours présente ---
        if snake.positions[0] == apple.positions:
            apple_sound.play()
            spawn_particles(apple.positions, color=APPLE_COLOR)
            snake.grow_snake()
            apple = Apple(snake)
            score += 1

            # Fait apparaître la pomme spéciale du mode, si ce n'est pas déjà fait
            if mode_key == "golden" and extra_apple is None and random.random() < 0.15:
                extra_apple = GoldenApple(snake, duration_ms=5000)
            elif mode_key == "ice_spicy" and extra_apple is None and random.random() < 0.2:
                if random.random() < 0.5:
                    extra_apple = IceApple(snake)
                else:
                    extra_apple = ChiliApple(snake)

        # --- Pomme dorée ---
        elif mode_key == "golden" and extra_apple and snake.positions[0] == extra_apple.positions:
            golden_sound.play()
            spawn_particles(extra_apple.positions, color=GOLDEN_APPLE_COLOR)
            snake.grow_snake()
            score += 3
            extra_apple = None

        # --- Pomme glace ---
        elif mode_key == "ice_spicy" and isinstance(extra_apple, IceApple) and snake.positions[0] == extra_apple.positions:
            ice_sound.play()
            spawn_particles(extra_apple.positions, color=ICE_APPLE_COLOR)
            snake.grow_snake()
            score += 1
            snake.speed_multiplier = 1.6  # plus lent
            speed_effect_end = pygame.time.get_ticks() + SPEED_EFFECT_DURATION
            extra_apple = None

        # --- Pomme piment ---
        elif mode_key == "ice_spicy" and isinstance(extra_apple, ChiliApple) and snake.positions[0] == extra_apple.positions:
            chili_sound.play()
            spawn_particles(extra_apple.positions, color=CHILI_APPLE_COLOR)
            snake.grow_snake()
            score += 2  # x2 points
            snake.speed_multiplier = 0.6  # plus rapide
            speed_effect_end = pygame.time.get_ticks() + SPEED_EFFECT_DURATION
            extra_apple = None

        # Golden expire toute seule après un moment
        if mode_key == "golden" and extra_apple and extra_apple.is_expired():
            extra_apple = None

        # Fin de l'effet de vitesse
        if speed_effect_end and pygame.time.get_ticks() > speed_effect_end:
            snake.speed_multiplier = 1.0
            speed_effect_end = 0

        hx, hy = snake.positions[0]
        ax, ay = apple.positions
        dist_apple = abs(hx - ax) + abs(hy - ay)

        if extra_apple:
            ex_, ey_ = extra_apple.positions
            dist_extra = abs(hx - ex_) + abs(hy - ey_)
            snake.mouth_open = min(dist_apple, dist_extra) <= 3
        else:
            snake.mouth_open = dist_apple <= 3

        draw_background(screen)
        draw_border(screen)
        if mode_key == "walls":
            draw_walls(screen, walls)
        snake.draw(screen)
        apple.draw(screen)

        if extra_apple:
            extra_apple.draw(screen)

        draw_particles(screen)
        display_score(screen, score)
        pygame.display.flip()
        clock.tick(FPS / snake.speed_multiplier)

        if len(snake.positions) == (GRID_SIZE - 2) * (GRID_SIZE - 2):
            victory_sound.play()
            victory_screen(screen, score)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False
            main()
            return

def main():
    mode_key = start_screen()
    if mode_key == "custom":
        mode_key = "classic"  # pas encore d'écran "sur mesure"
    run_game(mode_key)

if __name__ == "__main__":
    main()