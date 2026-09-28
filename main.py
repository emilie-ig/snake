import pygame
import sys
from config import FPS, GRID_SIZE, screen, apple_sound, gameover_sound, victory_sound
from snake import Snake
from apple import Apple
from fx import particles, spawn_particles, draw_particles
from ui import (
    draw_background, draw_border, display_score,
    game_over_screen, victory_screen, stun_animation, start_screen
)


def main():
    start_screen()
    particles.clear()
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

        if snake.positions[0] == apple.positions:
            apple_sound.play()
            spawn_particles(apple.positions)
            snake.grow_snake()
            apple = Apple(snake)
            score += 1

        hx, hy = snake.positions[0]
        ax, ay = apple.positions
        snake.mouth_open = abs(hx - ax) + abs(hy - ay) <= 3

        draw_background(screen)
        draw_border(screen)
        snake.draw(screen)
        apple.draw(screen)
        draw_particles(screen)
        display_score(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

        # La zone jouable fait (GRID_SIZE - 2) cases de côté
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