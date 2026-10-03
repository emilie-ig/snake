import pygame
import sys
import random
from config import (
    FPS, GRID_SIZE, CELL_SIZE, WALL_COLOR, screen, game_screen,
    GAME_X, GAME_Y, GAME_WIDTH, GAME_HEIGHT,
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


def blit_game():
    """Place la grille de jeu fixe au centre de la fenêtre."""
    screen.blit(game_screen, (GAME_X, GAME_Y))


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
            draw_background(game_screen)
            draw_border(game_screen)
            snake.draw(game_screen)
            apple.draw(game_screen)
            if golden_apple:
                golden_apple.draw(game_screen)
            draw_particles(game_screen)

            screen.fill((45, 28, 18))
            blit_game()
            display_score(screen, score)

            # Voile léger pour la lisibilité
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))

            # Affichage du chiffre du décompte
            text = font.render(str(count), True, (255, 255, 255))
            rect = text.get_rect(center=(GAME_X + GAME_WIDTH // 2, GAME_Y + GAME_HEIGHT // 2))
            screen.blit(text, rect)

            pygame.display.flip()
            clock.tick(FPS)

def generate_walls(snake, count=5, safe_radius=3):
    """Génère un petit nombre de murs éloignés du serpent au démarrage."""
    walls = []
    hx, hy = snake.positions[0]
    
    while len(walls) < count:
        x = random.randint(2, GRID_SIZE - 3)
        y = random.randint(2, GRID_SIZE - 3)
        pos = (x, y)
        
        # Distance de Manhattan par rapport à la tête du serpent
        dist_to_head = abs(hx - x) + abs(hy - y)
        
        if pos not in snake.positions and pos not in walls and dist_to_head > safe_radius:
            walls.append(pos)
            
    return walls

def add_wall(snake, apple, walls, golden_apple=None, special_apples=None):
    """Ajoute un mur supplémentaire sur une case libre."""
    occupied = set(snake.positions) | set(walls)
    occupied.add(apple.positions)
    if golden_apple:
        occupied.add(golden_apple.positions)
    if special_apples:
        occupied.update(sa.positions for sa in special_apples)

    # Zone d'interdiction (ne pas popper juste devant la tête du serpent)
    hx, hy = snake.positions[0]

    attempts = 0
    while attempts < 100:
        x = random.randint(2, GRID_SIZE - 3)
        y = random.randint(2, GRID_SIZE - 3)
        pos = (x, y)
        if pos not in occupied and (abs(hx - x) + abs(hy - y)) > 2:
            walls.append(pos)
            break
        attempts += 1


def draw_walls(surface, walls):
    for (x, y) in walls:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, WALL_COLOR, rect, border_radius=4)


def run_game(mode_key):
    particles.clear()
    clock = pygame.time.Clock()
    snake = Snake()
    
    # Gestion séparée pour la pomme dorée unique et la liste piment/glace
    golden_apple = None
    special_apples = []  # Contiendra les IceApple et ChiliApple

    walls = generate_walls(snake, count=5) if mode_key == "walls" else []
    apple = Apple(snake, walls)  # Passer les murs à la pomme
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
            blit_game()
            display_score(screen, score)
            draw_pause_overlay(screen)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # On dépile UNE seule direction par frame
        if direction_queue:
            next_direction = direction_queue.pop(0)
            snake.change_direction(next_direction)

        if not snake.move(walls):
            stun_animation(snake, apple, score)
            gameover_sound.play()
            
            selected_button = 0  # 0: Rejouer, 1: Menu principal
            font_btn = pygame.font.SysFont("arial", 28, bold=True)
            font_title = pygame.font.SysFont("arial", 56, bold=True)
            
            waiting = True
            while waiting:
                # 1. Redessine le jeu figé + un voile sombre
                blit_game()
                display_score(screen, score)
                
                overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                # Texte Game Over
                txt_gameover = font_title.render("GAME OVER", True, (231, 76, 60))
                rect_gameover = txt_gameover.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
                screen.blit(txt_gameover, rect_gameover)

                # Dimensions et positions des boutons
                center_x = screen.get_width() // 2
                center_y = screen.get_height() // 2 + 30
                btn_w, btn_h = 220, 50
                
                restart_rect = pygame.Rect(center_x - btn_w // 2, center_y, btn_w, btn_h)
                menu_rect = pygame.Rect(center_x - btn_w // 2, center_y + 65, btn_w, btn_h)

                # Couleurs des boutons
                green_color = (46, 204, 113) if selected_button == 0 else (39, 174, 96)
                menu_color = (231, 76, 60) if selected_button == 1 else (192, 57, 43)

                # Contour de sélection
                if selected_button == 0:
                    pygame.draw.rect(screen, (255, 255, 255), restart_rect.inflate(6, 6), border_radius=10)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), menu_rect.inflate(6, 6), border_radius=10)

                # Dessin des boutons
                pygame.draw.rect(screen, green_color, restart_rect, border_radius=8)
                pygame.draw.rect(screen, menu_color, menu_rect, border_radius=8)

                txt_restart = font_btn.render("Rejouer", True, (255, 255, 255))
                txt_menu = font_btn.render("Menu Principal", True, (255, 255, 255))

                screen.blit(txt_restart, txt_restart.get_rect(center=restart_rect.center))
                screen.blit(txt_menu, txt_menu.get_rect(center=menu_rect.center))

                pygame.display.flip()
                
                # 2. Gestion des événements
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEMOTION:
                        if restart_rect.collidepoint(event.pos):
                            selected_button = 0
                        elif menu_rect.collidepoint(event.pos):
                            selected_button = 1

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if restart_rect.collidepoint(event.pos):
                                run_game(mode_key)
                                return
                            elif menu_rect.collidepoint(event.pos):
                                main()
                                return

                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_UP, pygame.K_DOWN):
                            selected_button = 1 - selected_button
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                            if selected_button == 0:
                                run_game(mode_key)
                            else:
                                main()
                            return
                        elif event.key == pygame.K_ESCAPE:
                            main()
                            return

        # --- APPARITION ALEATOIRE TEMPORELLE DES GLACES / PIMENTS ---
        # ~1.5% de chance d'apparaître à chaque tick si le mode est activé
        if mode_key == "ice_spicy" and random.random() < 0.05:
            if random.random() < 0.5:
                special_apples.append(IceApple(snake))
            else:
                special_apples.append(ChiliApple(snake))

        # --- Pomme classique ---
        if snake.positions[0] == apple.positions:
            apple_sound.play()
            spawn_particles(apple.positions, color=APPLE_COLOR)
            snake.grow_snake()
            score += 1

            # Un nouveau mur poppe si on est dans le mode murs
            if mode_key == "walls":
                add_wall(snake, apple, walls, golden_apple, special_apples)

            # Réapparition de la pomme (sans popper sur les murs)
            apple = Apple(snake, walls)

            # La pomme dorée n'apparaît que si aucune n'est présente sur le plateau
            if mode_key == "golden" and golden_apple is None and random.random() < 0.2:
                golden_apple = GoldenApple(snake, duration_ms=5000)

        # --- Pomme dorée unique ---
        elif mode_key == "golden" and golden_apple and snake.positions[0] == golden_apple.positions:
            golden_sound.play()
            spawn_particles(golden_apple.positions, color=GOLDEN_APPLE_COLOR)
            snake.grow_snake()
            score += 3
            golden_apple = None

        # --- Pommes spéciales (Piments et Glaces) ---
        elif mode_key == "ice_spicy":
            for sp_apple in special_apples[:]:
                if snake.positions[0] == sp_apple.positions:
                    if isinstance(sp_apple, IceApple):
                        ice_sound.play()
                        spawn_particles(sp_apple.positions, color=ICE_APPLE_COLOR)
                        snake.grow_snake()
                        score += 1
                        snake.speed_multiplier = 1.6  # plus lent
                        snake.frozen = True
                        snake.boosted = False
                        speed_effect_end = pygame.time.get_ticks() + SPEED_EFFECT_DURATION
                    elif isinstance(sp_apple, ChiliApple):
                        chili_sound.play()
                        spawn_particles(sp_apple.positions, color=CHILI_APPLE_COLOR)
                        snake.grow_snake()
                        score += 2
                        snake.boosted = True
                        snake.frozen = False
                        snake.speed_multiplier = 0.6  # plus rapide
                        speed_effect_end = pygame.time.get_ticks() + SPEED_EFFECT_DURATION
                    
                    special_apples.remove(sp_apple)
                    break

        # Golden expire toute seule après un moment
        if mode_key == "golden" and golden_apple and golden_apple.is_expired():
            golden_apple = None

        # Fin de l'effet de vitesse
        if speed_effect_end and pygame.time.get_ticks() > speed_effect_end:
            snake.speed_multiplier = 1.0
            snake.boosted = False
            snake.frozen = False
            speed_effect_end = 0

        # --- Calcul de distance pour l'ouverture de la bouche ---
        hx, hy = snake.positions[0]
        all_targets = [apple.positions]
        if golden_apple:
            all_targets.append(golden_apple.positions)
        all_targets.extend([sa.positions for sa in special_apples])

        min_dist = min([abs(hx - tx) + abs(hy - ty) for tx, ty in all_targets])
        snake.mouth_open = min_dist <= 3

        # --- DESSIN DU JEU ---
        draw_background(game_screen)
        draw_border(game_screen)
        if mode_key == "walls":
            draw_walls(game_screen, walls)
        
        snake.draw(game_screen)
        apple.draw(game_screen)

        if golden_apple:
            golden_apple.draw(game_screen)

        for sp_apple in special_apples:
            sp_apple.draw(game_screen)

        draw_particles(game_screen)

        screen.fill((45, 28, 18))
        blit_game()
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
