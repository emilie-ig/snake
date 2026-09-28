import pygame
import sys
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_SIZE,
    BACKGROUND_COLOR, BACKGROUND_COLOR_2, BORDER_COLOR, SCORE_COLOR,
    SNAKE_HEAD_COLOR, SNAKE_TAIL_COLOR, screen, font, title_font,
    button_font, small_font, sss_sound, boing_sound
)


def draw_background(surface):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = BACKGROUND_COLOR if (x + y) % 2 == 0 else BACKGROUND_COLOR_2
            pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

def victory_screen(surface, score):
    draw_background(surface)
    victory_text = font.render("YOU WIN", True, SCORE_COLOR)
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    restart_text = font.render("Press Space to restart", True, SCORE_COLOR)
    surface.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 4))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

def stun_animation(snake, apple, score, duration=1500):
    sss_sound.stop()  # coupe un sifflement éventuel
    boing_sound.play()
    clock = pygame.time.Clock()
    start = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_background(screen)
        draw_border(screen)
        snake.draw(screen, stunned=True)
        apple.draw(screen)
        display_score(screen, score)
        pygame.display.flip()
        clock.tick(60)

def start_screen():
    clock = pygame.time.Clock()
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 245, 200, 65)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    return

        draw_background(screen)

        title = title_font.render("SNAKE", True, SNAKE_HEAD_COLOR)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        title_y = 85
        screen.blit(title, (title_x, title_y))

        subtitle = small_font.render("Mange les pommes et grandis !", True, SCORE_COLOR)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        screen.blit(subtitle, (subtitle_x, 180))

        pygame.draw.rect(screen, SNAKE_TAIL_COLOR, button_rect, border_radius=15)
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, button_rect, 3, border_radius=15)

        button_text = button_font.render("JOUER", True, SCORE_COLOR)
        button_x = SCREEN_WIDTH // 2 - button_text.get_width() // 2
        button_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (button_x, button_y))

        start_text = small_font.render("ESPACE ou ENTRÉE pour jouer", True, SCORE_COLOR)
        start_x = SCREEN_WIDTH // 2 - start_text.get_width() // 2
        screen.blit(start_text, (start_x, 390))

        quit_text = small_font.render("ÉCHAP pour quitter", True, SCORE_COLOR)
        quit_x = SCREEN_WIDTH // 2 - quit_text.get_width() // 2
        screen.blit(quit_text, (quit_x, 425))

        draw_border(screen)
        pygame.display.flip()
        clock.tick(60)