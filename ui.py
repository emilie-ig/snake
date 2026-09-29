import pygame
import sys
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GAME_WIDTH, GAME_HEIGHT, GAME_X, GAME_Y,
    SCORE_PANEL_X, SCORE_PANEL_Y, SCORE_PANEL_WIDTH, SCORE_PANEL_HEIGHT,
    CELL_SIZE, GRID_SIZE,
    BACKGROUND_COLOR, BACKGROUND_COLOR_2, BORDER_COLOR, SCORE_COLOR,
    LANGUAGES, screen, game_screen, font, sss_sound, boing_sound
)


def draw_background(surface):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = BACKGROUND_COLOR if (x + y) % 2 == 0 else BACKGROUND_COLOR_2
            pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_border(surface):
    pygame.draw.rect(surface, BORDER_COLOR, pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT), CELL_SIZE)


def draw_menu_background(surface):
    surface.fill((45, 28, 18))

    for y in range(0, SCREEN_HEIGHT, 25):
        pygame.draw.line(surface, (55, 34, 21), (0, y), (SCREEN_WIDTH, y), 1)

    for x in range(0, SCREEN_WIDTH, 25):
        pygame.draw.line(surface, (55, 34, 21), (x, 0), (x, SCREEN_HEIGHT), 1)


def display_score(surface, score):
    panel_rect = pygame.Rect(SCORE_PANEL_X, SCORE_PANEL_Y, SCORE_PANEL_WIDTH, SCORE_PANEL_HEIGHT)
    pygame.draw.rect(surface, (30, 24, 18), panel_rect, border_radius=18)
    pygame.draw.rect(surface, (65, 48, 28), panel_rect, 2, border_radius=18)
    pygame.draw.rect(surface, BORDER_COLOR, (panel_rect.x, panel_rect.y, panel_rect.width, 7), border_radius=7)

    score_label = pygame.font.SysFont("arial", 20, bold=True).render("SCORE", True, (175, 175, 175))
    score_label_rect = score_label.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
    surface.blit(score_label, score_label_rect)

    score_font = pygame.font.SysFont("arial", 58, bold=True)
    score_text = score_font.render(str(score), True, SCORE_COLOR)
    score_text_rect = score_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 92))
    surface.blit(score_text, score_text_rect)

    pygame.draw.line(surface, (80, 65, 45), (panel_rect.x + 25, panel_rect.y + 125), (panel_rect.right - 25, panel_rect.y + 125), 1)

    info_font = pygame.font.SysFont("arial", 15)
    info_text = info_font.render("P  •  PAUSE", True, (150, 150, 150))
    info_rect = info_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 150))
    surface.blit(info_text, info_rect)


def game_over_screen(surface, score):
    """Écran de Game Over interactif avec boutons Rejouer et Menu."""
    surface.fill((20, 15, 12))
    
    # Carte centrale
    card_width, card_height = 440, 340
    card_rect = pygame.Rect(
        (SCREEN_WIDTH - card_width) // 2,
        (SCREEN_HEIGHT - card_height) // 2,
        card_width,
        card_height
    )
    
    # Fond et bordure
    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, (35, 25, 20, 240), (0, 0, card_width, card_height), border_radius=16)
    surface.blit(card_surface, card_rect.topleft)
    pygame.draw.rect(surface, (220, 50, 50), card_rect, width=3, border_radius=16)

    # Polices
    font_title = pygame.font.SysFont("arial", 44, bold=True)
    font_score_label = pygame.font.SysFont("arial", 16, bold=True)
    font_score_val = pygame.font.SysFont("arial", 48, bold=True)
    font_btn = pygame.font.SysFont("arial", 16, bold=True)

    # Titre "GAME OVER"
    title_surf = font_title.render("GAME OVER", True, (255, 75, 75))
    title_rect = title_surf.get_rect(center=(card_rect.centerx, card_rect.y + 45))
    surface.blit(title_surf, title_rect)

    # Séparateur
    pygame.draw.line(surface, (80, 50, 40), (card_rect.x + 40, card_rect.y + 80), (card_rect.right - 40, card_rect.y + 80), 1)

    # Score
    lbl_surf = font_score_label.render("SCORE FINAL", True, (160, 150, 140))
    lbl_rect = lbl_surf.get_rect(center=(card_rect.centerx, card_rect.y + 105))
    surface.blit(lbl_surf, lbl_rect)

    val_surf = font_score_val.render(str(score), True, SCORE_COLOR)
    val_rect = val_surf.get_rect(center=(card_rect.centerx, card_rect.y + 150))
    surface.blit(val_surf, val_rect)

    # --- BOUTONS ---
    mouse_pos = pygame.mouse.get_pos()

    # Bouton REJOUER (Entrée)
    restart_btn_rect = pygame.Rect(card_rect.centerx - 180, card_rect.y + 220, 175, 48)
    is_restart_hovered = restart_btn_rect.collidepoint(mouse_pos)
    btn_restart_color = (210, 50, 50) if is_restart_hovered else (170, 35, 35)
    
    pygame.draw.rect(surface, btn_restart_color, restart_btn_rect, border_radius=10)
    pygame.draw.rect(surface, (255, 100, 100), restart_btn_rect, width=2, border_radius=10)

    restart_surf = font_btn.render("REJOUER [↵]", True, (255, 255, 255))
    restart_rect = restart_surf.get_rect(center=restart_btn_rect.center)
    surface.blit(restart_surf, restart_rect)

    # Bouton MENU
    menu_btn_rect = pygame.Rect(card_rect.centerx + 5, card_rect.y + 220, 175, 48)
    is_menu_hovered = menu_btn_rect.collidepoint(mouse_pos)
    btn_menu_color = (80, 80, 100) if is_menu_hovered else (50, 50, 65)

    pygame.draw.rect(surface, btn_menu_color, menu_btn_rect, border_radius=10)
    pygame.draw.rect(surface, (140, 140, 160), menu_btn_rect, width=2, border_radius=10)

    menu_surf = font_btn.render("MENU", True, (255, 255, 255))
    menu_rect = menu_surf.get_rect(center=menu_btn_rect.center)
    surface.blit(menu_surf, menu_rect)

    return restart_btn_rect, menu_btn_rect

def victory_screen(surface, score):
    surface.fill((45, 28, 18))
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

        draw_background(game_screen)
        draw_border(game_screen)
        snake.draw(game_screen, stunned=True)
        apple.draw(game_screen)

        screen.fill((45, 28, 18))
        screen.blit(game_screen, (GAME_X, GAME_Y))
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
    box_width = 700
    box_height = 50
    box_rect = pygame.Rect((SCREEN_WIDTH - box_width) // 2, 415, box_width, box_height)
    border_radius = 10

    # Surface du fond avec masque arrondi strict
    box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    box_surface.fill((15, 23, 42, 230))

    mask = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, box_rect.width, box_rect.height), border_radius=border_radius)
    box_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    screen.blit(box_surface, box_rect.topleft)

    # Contour doré fin
    pygame.draw.rect(screen, (255, 215, 0), box_rect, 2, border_radius=border_radius)

    # Petite icône "i" d'information
    icon_bg = pygame.Rect(box_rect.x + 12, box_rect.y + 14, 22, 22)
    pygame.draw.circle(screen, (255, 215, 0), icon_bg.center, 11)
    icon_surf = font_icon.render("i", True, (15, 23, 42))
    screen.blit(icon_surf, icon_surf.get_rect(center=icon_bg.center))

    # Affichage intelligent du texte (mise en valeur si format "Titre : Description")
    text_x = box_rect.x + 45
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
    draw_menu_background(screen)

    font_title = pygame.font.SysFont("arial", 42, bold=True)
    font_sub = pygame.font.SysFont("arial", 17)
    font_card = pygame.font.SysFont("arial", 14, bold=True)
    font_desc = pygame.font.SysFont("arial", 14)
    font_icon = pygame.font.SysFont("arial", 14, bold=True)
    font_play = pygame.font.SysFont("arial", 24, bold=True)

    title_surf = font_title.render(lang_data["title"], True, (1, 252, 128))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 45))
    screen.blit(title_surf, title_rect)

    draw_flag(screen, current_lang, flag_rect)

    sub_surf = font_sub.render(lang_data["select_mode"], True, (200, 200, 200))
    sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 83))
    screen.blit(sub_surf, sub_rect)

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
        0: pygame.Rect(95, 150, 130, 180),
        1: pygame.Rect(240, 150, 130, 180),
        2: pygame.Rect(385, 150, 130, 180),
        3: pygame.Rect(530, 150, 130, 180),
        4: pygame.Rect(675, 150, 130, 180)
    }

    flag_rect = pygame.Rect(SCREEN_WIDTH - 55, 20, 35, 24)
    play_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 490, 200, 52)

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
