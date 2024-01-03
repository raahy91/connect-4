import connect4
import pygame
import pygame.gfxdraw
import util
import sys

# Init
pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")
logo = pygame.image.load('c4.png')
logo_rect = logo.get_rect(center=(width // 2, height // 2 - 150))

# Boutons
font_path = "Orbitron-Black.ttf"
font = pygame.font.Font(font_path, 30)
easy_button_text = font.render("EASY", True, (0, 0, 0))
easy_button_rect = easy_button_text.get_rect(center=(width // 2, height // 2 + 100))
easy_button_rect.inflate_ip(74, 20)

normal_button_text = font.render("NORMAL", True, (0, 0, 0))
normal_button_rect = normal_button_text.get_rect(center=(width // 2, height // 2 + 170))
normal_button_rect.inflate_ip(20, 20)

hard_button_text = font.render("HARD", True, (0, 0, 0))
hard_button_rect = hard_button_text.get_rect(center=(width // 2, height // 2 + 240))
hard_button_rect.inflate_ip(70, 20)

quit_button_text = font.render("QUIT", True, (0, 0, 0))
quit_button_rect = quit_button_text.get_rect(center=(width // 2, height // 2 + 310))
quit_button_rect.inflate_ip(90, 20)

back_path = pygame.image.load('wp2.jpg')
background_image = pygame.transform.scale(back_path, (width, height))


def run_game(difficulty):
    # Boutons de fin de partie
    restart_text = font.render("RESTART", True, (0, 0, 0))
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2))
    restart_rect.inflate_ip(74, 20)

    change_text = font.render("CHANGE", True, (0, 0, 0))
    difficulty_text = font.render("DIFFICULTY", True, (0, 0, 0))
    change_rect = change_text.get_rect(center=(width // 2, height // 2 + 80))
    difficulty_rect = difficulty_text.get_rect(center=(width // 2, height // 2 + 110))
    total_width = max(change_rect.width, difficulty_rect.width) + 40
    total_height = (difficulty_rect.bottom - change_rect.top) + 20
    change_diff_rect = pygame.Rect(width // 2 - total_width // 2, change_rect.top - 10,
                                   total_width, total_height)

    over_quit_text = font.render("QUIT", True, (0, 0, 0))
    over_quit_rect = restart_text.get_rect(center=(width // 2, height // 2 + 190))
    over_quit_rect.inflate_ip(74, 20)

    # Score en haut de l'écran
    to_score = True
    player_wins = 0
    computer_wins = 0
    p_t = font.render("PLAYER", True, util.light_turq)
    c_t = font.render("COMPUTER", True, util.light_grey)

    # Settings du jeu
    c4 = connect4.Connect4()
    board_w, board_h = 672, 578
    x, y = (width - board_w) // 2, (height - board_h) // 2 + 40
    radius, buffer = 40, 14
    y_falling_pos = y - radius
    x_falling_pos = 0
    computer_x = 5000
    computer_y = y_falling_pos

    # Flags et valeurs arbitraires
    player_turn = True
    player_last_played = True
    y_falling = False
    valid_move = False
    move_chosen = False
    in_computer_loop = False
    col = -1
    temp_col = -1

    # Positions initiales des trous
    pixel_positions = []
    x_pixel_centers = []
    y_pixel_centers = []
    for j in range(6):
        for i in range(7):
            x_pos = x + (2 * i + 1) * radius + (i + 1) * buffer
            y_pos = y + (2 * j + 1) * radius + (j + 1) * buffer
            pixel_positions.append((x_pos, y_pos))
            if x_pos not in x_pixel_centers:
                x_pixel_centers.append(x_pos)
            if y_pos not in y_pixel_centers:
                y_pixel_centers.append(y_pos)

    # Détermine les intervalles des colonnes pour placer les jetons selon le clic
    x_intervals = [[x + buffer, x + 2 * radius + 3 * buffer / 2]]
    for i in range(5):
        i += 1
        x_intervals.append([x + 2 * i * radius + (2 * i + 1) * buffer / 2,
                            (x + 2 * (i + 1) * radius + (2 * i + 2) * buffer / 2) + buffer])
    x_intervals.append([x + 12 * radius + 13 * buffer / 2, x + 14 * radius + 7 * buffer])

    # Game loop
    game_over = False
    running_game = True
    while running_game:
        screen.blit(background_image, (0, 0))

        # Listeners events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if restart_rect.collidepoint(event.pos):
                    c4.reset()
                    game_over = False
                    to_score = True
                if change_diff_rect.collidepoint(event.pos):
                    game_over = False
                    running_game = False
                if over_quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not y_falling and player_turn:
                y_falling = True
                x_falling_pos = util.adjust_mouse_pos(pygame.mouse.get_pos()[0], x, radius, board_w, buffer)
                for i in range(len(x_intervals)):
                    if x_intervals[i][0] <= x_falling_pos <= x_intervals[i][1]:
                        x_falling_pos, col = x_pixel_centers[i], i
                        break

        # Validation du jeu du joueur
        if player_turn and not game_over:
            if c4.is_valid_move(col):
                temp_col, valid_move = col, True
            else:
                if col != -1:
                    y_falling, x_falling_pos = False, 0
            col = -1

            # Chute du jeton et mise à jour de moves
            if y_falling and valid_move:
                y_height = c4.find_height(temp_col, y_pixel_centers)
                y_falling_pos += 1.25
                if y_falling_pos >= y_height:
                    c4.set_a_move(player_turn, temp_col)
                    y_falling, valid_move = False, False
                    x_falling_pos, y_falling_pos = 0, y - radius
                    player_last_played = player_turn
                    player_turn = not player_turn
        elif not game_over:
            # Jeu et chute de l'ordinateur
            if not move_chosen:
                if difficulty == "Easy":
                    computer_move = c4.minimax_agent(2, 1)
                elif difficulty == "Normal":
                    computer_move = c4.minimax_agent(2, 2)
                else:
                    computer_move = c4.minimax_agent(2, 4)
                computer_x = x_pixel_centers[computer_move[0]]
                y_height = c4.find_height(computer_move[0], y_pixel_centers)
                move_chosen = True
            computer_y += 1.25
            if computer_y >= y_height:
                c4.play_computer_move(computer_move[1])
                computer_y = y - radius
                player_last_played = player_turn
                player_turn = not player_turn
                move_chosen = False
                in_computer_loop = False

        # Positions des tokens
        turq_token = util.create_gradient_circle(radius, util.light_turq, util.dark_turq)
        grey_token = util.create_gradient_circle(radius, util.light_grey, util.dark_grey)
        for i in range(len(pixel_positions)):
            if c4.moves[i] == 0:
                pygame.gfxdraw.aacircle(screen, pixel_positions[i][0], pixel_positions[i][1], radius, util.BLUE)
            elif c4.moves[i] == 1:
                screen.blit(turq_token, (pixel_positions[i][0] - radius, pixel_positions[i][1] - radius))
            else:
                screen.blit(grey_token, (pixel_positions[i][0] - radius, pixel_positions[i][1] - radius))

        # Ajustement de la position de la souris en x pour ne pas dépasser le board
        mouse_x = util.adjust_mouse_pos(pygame.mouse.get_pos()[0], x, radius, board_w, buffer)
        mouse_x = mouse_x if x_falling_pos == 0 else x_falling_pos

        # Loop d'action
        if player_turn and not game_over:
            screen.blit(turq_token, (mouse_x - radius, y_falling_pos - radius))
        elif not game_over:
            if in_computer_loop:
                screen.blit(grey_token, (computer_x - radius, computer_y - radius))
            else:
                in_computer_loop = True

        # Score en haut de l'écran
        score = font.render(str(player_wins) + " - " + str(computer_wins), True, (250, 250, 250))
        screen.blit(p_t, (405, 20))
        screen.blit(score, (560, 20))
        screen.blit(c_t, (655, 20))

        # Si quelqu'un gagne
        game_state = c4.game_over(player_last_played)
        if game_state != "Continue":

            game_over = True
            over_mouse_pos = pygame.mouse.get_pos()

            # Winner
            winner = "You lose!" if player_turn else "You win!"
            if game_state == "Draw":
                winner = "Draw!"
            else:
                # Ligne qui parcoure les jetons gagnants
                winning_tokens = c4.get_winners()
                start, end = pixel_positions[winning_tokens[0]], pixel_positions[winning_tokens[1]]
                color = util.light_turq if player_turn else util.dark_grey
                pygame.draw.line(screen, color, start, end, 5)

            # Score
            if to_score and game_state == "Win":
                player_wins = player_wins if player_turn else player_wins + 1
                computer_wins = computer_wins + 1 if player_turn else computer_wins
                to_score = False

            # Box de fin de jeu
            text = font.render(winner, True, util.BLACK)
            diff_x, diff_y = 350, 150
            text_rect = text.get_rect(center=(x + board_w // 2, y + 50 + diff_y / 2))
            pygame.draw.rect(screen, util.GREY, (x + diff_x / 2, y + diff_y / 2, board_w - diff_x, board_h - diff_y))
            pygame.draw.rect(screen, util.BLACK, (x + diff_x / 2, y + diff_y / 2, board_w - diff_x, board_h - diff_y),
                             5)
            screen.blit(text, text_rect)

            # Boutons de fin de jeu
            restart_color = util.DARK_GREY if restart_rect.collidepoint(over_mouse_pos) else util.GREY
            pygame.draw.rect(screen, restart_color, restart_rect)
            pygame.draw.rect(screen, util.BLACK, restart_rect, 2)
            screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

            change_diff_color = util.DARK_GREY if change_diff_rect.collidepoint(over_mouse_pos) else util.GREY
            pygame.draw.rect(screen, change_diff_color, change_diff_rect)
            pygame.draw.rect(screen, (0, 0, 0), change_diff_rect, 2)

            over_quit_color = util.DARK_GREY if over_quit_rect.collidepoint(over_mouse_pos) else util.GREY
            pygame.draw.rect(screen, over_quit_color, over_quit_rect)
            pygame.draw.rect(screen, util.BLACK, over_quit_rect, 2)
            screen.blit(over_quit_text, over_quit_text.get_rect(center=over_quit_rect.center))

            # Dessiner les textes du bouton Change Difficulty
            screen.blit(change_text, change_rect)
            screen.blit(difficulty_text, difficulty_rect)

        pygame.display.flip()


# Menu
running_menu = True
while running_menu:

    # Listeners events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button_rect.collidepoint(event.pos):
                run_game("Easy")
            if normal_button_rect.collidepoint(event.pos):
                run_game("Normal")
            if hard_button_rect.collidepoint(event.pos):
                run_game("Hard")
            if quit_button_rect.collidepoint(event.pos):
                running_menu = False

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background_image, (0, 0))

    # Logo Connect4
    screen.blit(logo, logo_rect)

    # Boutons du menu
    easy_button_color = util.DARK_GREY if easy_button_rect.collidepoint(mouse_pos) else util.GREY
    normal_button_color = util.DARK_GREY if normal_button_rect.collidepoint(mouse_pos) else util.GREY
    hard_button_color = util.DARK_GREY if hard_button_rect.collidepoint(mouse_pos) else util.GREY
    quit_button_color = util.DARK_GREY if quit_button_rect.collidepoint(mouse_pos) else util.GREY

    pygame.draw.rect(screen, easy_button_color, easy_button_rect)
    pygame.draw.rect(screen, util.BLACK, easy_button_rect, 2)
    screen.blit(easy_button_text, easy_button_text.get_rect(center=easy_button_rect.center))

    pygame.draw.rect(screen, normal_button_color, normal_button_rect)
    pygame.draw.rect(screen, util.BLACK, normal_button_rect, 2)
    screen.blit(normal_button_text, normal_button_text.get_rect(center=normal_button_rect.center))

    pygame.draw.rect(screen, hard_button_color, hard_button_rect)
    pygame.draw.rect(screen, util.BLACK, hard_button_rect, 2)
    screen.blit(hard_button_text, hard_button_text.get_rect(center=hard_button_rect.center))

    pygame.draw.rect(screen, quit_button_color, quit_button_rect)
    pygame.draw.rect(screen, util.BLACK, quit_button_rect, 2)
    screen.blit(quit_button_text, quit_button_text.get_rect(center=quit_button_rect.center))

    pygame.display.flip()

pygame.quit()
sys.exit()
