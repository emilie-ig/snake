import pygame
import sys
import random
from config import (
    FPS, GRID_SIZE, screen, APPLE_COLOR, GOLDEN_APPLE_COLOR,
    apple_sound, golden_sound, gameover_sound, victory_sound
)
from snake import Snake
from apple import Apple, GoldenApple
from fx import particles, spawn_particles, draw_particles
from ui import (
    draw_background, draw_border, display_score,
    game_over_screen, victory_screen, stun_animation, start_screen
)


def draw_pause_overlay(screen):
    """Dessine un voile gris semi-transparent et l'affichage PAUSE."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    # Remplissage gris avec une transparence alpha de 160 (sur 255)
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


def main():
    start_screen()
    particles.clear()
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple(snake)
    golden_apple = None
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
                        # Si on était en pause, on fait le décompte avant de reprendre
                        run_countdown(screen, snake, apple, golden_apple, score)
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

        # Pomme classique
        if snake.positions[0] == apple.positions:
            apple_sound.play()
            spawn_particles(apple.positions, color=APPLE_COLOR)
            snake.grow_snake()
            apple = Apple(snake)
            score += 1

            if golden_apple is None and random.random() < 0.15:
                golden_apple = GoldenApple(snake, duration_ms=5000)

        # Pomme dorée
        elif golden_apple and snake.positions[0] == golden_apple.positions:
            golden_sound.play()
            spawn_particles(golden_apple.positions, color=GOLDEN_APPLE_COLOR)
            snake.grow_snake()
            score += 3
            golden_apple = None

        if golden_apple and golden_apple.is_expired():
            golden_apple = None

        hx, hy = snake.positions[0]
        ax, ay = apple.positions
        dist_apple = abs(hx - ax) + abs(hy - ay)
        
        if golden_apple:
            gx, gy = golden_apple.positions
            dist_golden = abs(hx - gx) + abs(hy - gy)
            snake.mouth_open = min(dist_apple, dist_golden) <= 3
        else:
            snake.mouth_open = dist_apple <= 3

        draw_background(screen)
        draw_border(screen)
        snake.draw(screen)
        apple.draw(screen)
        
        if golden_apple:
            golden_apple.draw(screen)

        draw_particles(screen)
        display_score(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

        if len(snake.positions) == (GRID_SIZE - 2) * (GRID_SIZE - 2):
            victory_sound.play()
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


if __name__ == "__main__":
    main()