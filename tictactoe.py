"""A simple tic-tac-toe game in pygame, made for two players."""

import pygame
import numpy as np
import sys
import game_setup as setup

screen = setup.start_game()

game = setup.Game(screen)
board = np.zeros(game.size)

player = 1
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(sysfont, setup.OFFSET)


def draw_figures(pos: tuple, player_num: int):
    if player_num == 1:
        pygame.draw.circle(screen, setup.LINE_COLOR, pos, 60, 15)
    else:
        pygame.draw.line(screen, setup.LINE_COLOR, (pos[0] - 60, pos[1] - 60), (pos[0] + 60, pos[1] + 60), 15)
        pygame.draw.line(screen, setup.LINE_COLOR, (pos[0] + 60, pos[1] - 60), (pos[0] - 60, pos[1] + 60), 15)


while True:
    for event in pygame.event.get():
        game.new_game_menu(event, font)

        if game.check_win():
            text = font.render(f"Player {player} wins!", True, setup.LINE_COLOR)
            screen.blit(text, (setup.WIDTH / 2 - text.get_width() / 2, text.get_height() / 2))
            game.game_over = True
        if game.is_board_full():
            game.game_over = True
        if event.type == pygame.QUIT:
            sys.exit()
        if game.single_player:
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.new_game:
                x, y = pygame.mouse.get_pos()

                if x < setup.WIDTH / 3:
                    col = 0
                elif x < setup.WIDTH / 3 * 2:
                    col = 1
                elif x < setup.WIDTH:
                    col = 2
                else:
                    col = None

                if y < setup.HEIGHT / 3:
                    row = 0
                elif y < setup.HEIGHT / 3 * 2:
                    row = 1
                elif y < setup.HEIGHT:
                    row = 2
                else:
                    row = None

                if row is not None and col is not None and game.available_square(row, col):
                    game.mark_square(row, col, player)
                    # center the x's and o's in each box
                    figure_x = (col * setup.WIDTH / 3) + setup.WIDTH / 6
                    figure_y = (row * setup.HEIGHT / 3) + setup.HEIGHT / 6

                    draw_figures((figure_x, figure_y), player)
                    if player == 1:
                        player = 2
                    else:
                        player = 1
        if game.multi_player:
            # TODO add multiplayer code using computer as player 2
            pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.new_game = True
                game.reset_game()

        if game.game_over:
            restart_text = font.render("Press R to restart", True, setup.LINE_COLOR)
            screen.blit(restart_text, (setup.WIDTH / 3 - restart_text.get_width(), setup.HEIGHT
                                       - restart_text.get_height()))
            quit_text = font.render("Press SPACE to quit", True, setup.LINE_COLOR)
            screen.blit(quit_text, (setup.WIDTH - quit_text.get_width(), setup.HEIGHT - quit_text.get_height()))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit("Thanks for playing!")

    pygame.display.update()
