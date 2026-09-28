import pygame
import sys
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_SIZE,
    BACKGROUND_COLOR, BACKGROUND_COLOR_2, BORDER_COLOR, SCORE_COLOR,
    LANGUAGES, screen, font, sss_sound, boing_sound
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
    sss_sound.stop()
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


def draw_grid_card(screen, rect, title, bg_image, is_highlighted, font_title):
    """Dessine une carte de mode avec des coins arrondis"""
    border_radius = 12
    border_color = (255, 215, 0) if is_highlighted else (100, 100, 120)
    border_width = 4 if is_highlighted else 2

    card_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    if bg_image:
        scaled_image = pygame.transform.smoothscale(bg_image, (rect.width, rect.height))
        card_surface.blit(scaled_image, (0, 0))
    else:
        bg_color = (60, 80, 110) if is_highlighted else (40, 40, 50)
        card_surface.fill(bg_color)

    label_height = 34
    overlay = pygame.Surface((rect.width, label_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    card_surface.blit(overlay, (0, rect.height - label_height))

    # Masque pour garantir des coins parfaitement arrrondis
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, rect.width, rect.height), border_radius=border_radius)
    card_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    screen.blit(card_surface, rect.topleft)
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=border_radius)

    title_surf = font_title.render(title, True, (255, 255, 255))
    if title_surf.get_width() > rect.width - 10:
        small_font = pygame.font.SysFont("arial", 12, bold=True)
        title_surf = small_font.render(title, True, (255, 255, 255))

    title_rect = title_surf.get_rect(center=(rect.centerx, rect.bottom - (label_height // 2)))
    screen.blit(title_surf, title_rect)


def draw_description_box(screen, desc, font_desc, font_icon):
    """Bandeau explicatif avec coins arrondis masqués et icône info"""
    box_rect = pygame.Rect(20, 375, 455, 44)
    border_radius = 10

    # Surface du fond avec masque arrondi strict
    box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    box_surface.fill((15, 23, 42, 230))  # Fond bleu nuit très sobre

    mask = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, box_rect.width, box_rect.height), border_radius=border_radius)
    box_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    screen.blit(box_surface, box_rect.topleft)

    # Contour doré fin
    pygame.draw.rect(screen, (255, 215, 0), box_rect, 2, border_radius=border_radius)

    # Petite icône "i" d'information
    icon_bg = pygame.Rect(box_rect.x + 10, box_rect.y + 11, 22, 22)
    pygame.draw.circle(screen, (255, 215, 0), icon_bg.center, 11)
    icon_surf = font_icon.render("i", True, (15, 23, 42))
    screen.blit(icon_surf, icon_surf.get_rect(center=icon_bg.center))

    # Affichage intelligent du texte (mise en valeur si format "Titre : Description")
    text_x = box_rect.x + 40
    if ":" in desc:
        parts = desc.split(":", 1)
        prefix_surf = font_desc.render(parts[0] + " :", True, (255, 215, 0))
        suffix_surf = font_desc.render(parts[1], True, (230, 230, 230))

        screen.blit(prefix_surf, (text_x, box_rect.centery - prefix_surf.get_height() // 2))
        screen.blit(suffix_surf, (text_x + prefix_surf.get_width() + 5, box_rect.centery - suffix_surf.get_height() // 2))
    else:
        desc_surf = font_desc.render(desc, True, (230, 230, 230))
        screen.blit(desc_surf, (text_x, box_rect.centery - desc_surf.get_height() // 2))


def draw_flag(screen, current_lang, rect):
    """Dessine le drapeau FR ou EN."""
    pygame.draw.rect(screen, (200, 200, 200), rect, 1, border_radius=4)
    w, h = rect.width, rect.height

    if current_lang == "FR":
        pygame.draw.rect(screen, (0, 38, 84), (rect.x, rect.y, w // 3, h))
        pygame.draw.rect(screen, (255, 255, 255), (rect.x + w // 3, rect.y, w // 3, h))
        pygame.draw.rect(screen, (206, 17, 38), (rect.x + 2 * (w // 3), rect.y, w - 2 * (w // 3), h))
    else:
        pygame.draw.rect(screen, (1, 33, 105), rect)
        pygame.draw.line(screen, (255, 255, 255), rect.topleft, rect.bottomright, 3)
        pygame.draw.line(screen, (255, 255, 255), rect.topright, rect.bottomleft, 3)
        pygame.draw.rect(screen, (255, 255, 255), (rect.x + w // 2 - 3, rect.y, 6, h))
        pygame.draw.rect(screen, (255, 255, 255), (rect.x, rect.y + h // 2 - 3, w, 6))
        pygame.draw.rect(screen, (200, 16, 46), (rect.x + w // 2 - 2, rect.y, 4, h))
        pygame.draw.rect(screen, (200, 16, 46), (rect.x, rect.y + h // 2 - 2, w, 4))


def render_start_menu(screen, current_lang, active_index, mode_keys, rects_map, flag_rect, play_btn_rect, is_play_hovered):
    """Rendu global du menu principal."""
    lang_data = LANGUAGES[current_lang]
    draw_background(screen)

    font_title = pygame.font.SysFont("arial", 36, bold=True)
    font_sub = pygame.font.SysFont("arial", 15)
    font_card = pygame.font.SysFont("arial", 13, bold=True)
    font_desc = pygame.font.SysFont("arial", 13)
    font_icon = pygame.font.SysFont("arial", 14, bold=True)
    font_play = pygame.font.SysFont("arial", 22, bold=True)

    title_surf = font_title.render(lang_data["title"], True, (1, 252, 128))
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 30))
    screen.blit(title_surf, title_rect)

    draw_flag(screen, current_lang, flag_rect)

    sub_surf = font_sub.render(lang_data["select_mode"], True, (200, 200, 200))
    screen.blit(sub_surf, (20, 55))

    for i, key in enumerate(mode_keys):
        mode_info = lang_data["modes"][key]
        is_highlighted = (i == active_index)
        rect = rects_map[i]

        bg_image = None
        if "icon" in mode_info:
            try:
                bg_image = pygame.image.load(mode_info["icon"]).convert_alpha()
            except Exception:
                bg_image = None

        draw_grid_card(screen, rect, mode_info["title"], bg_image, is_highlighted, font_card)

    active_key = mode_keys[active_index]
    active_desc = lang_data["modes"][active_key]["desc"]
    draw_description_box(screen, active_desc, font_desc, font_icon)

    btn_color = (0, 200, 100) if is_play_hovered else (0, 140, 80)
    pygame.draw.rect(screen, btn_color, play_btn_rect, border_radius=12)
    pygame.draw.rect(screen, (1, 252, 128), play_btn_rect, 3, border_radius=12)

    play_label = "JOUER" if current_lang == "FR" else "PLAY"
    play_surf = font_play.render(play_label, True, (255, 255, 255))
    play_text_rect = play_surf.get_rect(center=play_btn_rect.center)
    screen.blit(play_surf, play_text_rect)

def start_screen():
    """Gère le survol, la navigation et le lancement."""
    current_lang = "FR"
    selected_index = 0
    mode_keys = list(LANGUAGES[current_lang]["modes"].keys())
    clock = pygame.time.Clock()

    rects_map = {
        0: pygame.Rect(20, 80, 210, 280),
        1: pygame.Rect(245, 80, 110, 132),
        2: pygame.Rect(365, 80, 110, 132),
        3: pygame.Rect(245, 228, 110, 132),
        4: pygame.Rect(365, 228, 110, 132)
    }

    flag_rect = pygame.Rect(SCREEN_WIDTH - 55, 15, 35, 24)
    play_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 90, 432, 180, 48)

    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        hovered_index = None
        is_play_hovered = play_btn_rect.collidepoint(mouse_pos)

        for idx, rect in rects_map.items():
            if rect.collidepoint(mouse_pos):
                hovered_index = idx
                selected_index = idx
                break

        active_index = hovered_index if hovered_index is not None else selected_index

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if flag_rect.collidepoint(mouse_pos):
                        current_lang = "EN" if current_lang == "FR" else "FR"
                        mode_keys = list(LANGUAGES[current_lang]["modes"].keys())
                    elif hovered_index is not None or is_play_hovered:
                        waiting = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if selected_index in (1, 3):
                        selected_index = 0
                    elif selected_index in (2, 4):
                        selected_index -= 1
                elif event.key == pygame.K_RIGHT:
                    if selected_index == 0:
                        selected_index = 1
                    elif selected_index in (1, 3):
                        selected_index += 1
                elif event.key == pygame.K_UP:
                    if selected_index == 3:
                        selected_index = 1
                    elif selected_index == 4:
                        selected_index = 2
                elif event.key == pygame.K_DOWN:
                    if selected_index == 1:
                        selected_index = 3
                    elif selected_index == 2:
                        selected_index = 4
                elif event.key == pygame.K_l:
                    current_lang = "EN" if current_lang == "FR" else "FR"
                    mode_keys = list(LANGUAGES[current_lang]["modes"].keys())
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    waiting = False

        render_start_menu(
            screen, current_lang, active_index, mode_keys,
            rects_map, flag_rect, play_btn_rect, is_play_hovered
        )
        pygame.display.flip()
        clock.tick(30)

    return mode_keys[selected_index]