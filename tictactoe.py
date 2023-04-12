"""A simple tic-tac-toe game in pygame. Contains both single player and multiplayer modes."""
import pygame
import sys
import game_setup as setup

screen = setup.start_game()

# create game object and potential player objects
game = setup.Game(screen)
player1 = setup.Player(1)
player2 = setup.Player(2)
com_player = setup.ComputerPlayer(2)

sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(sysfont, setup.OFFSET)

while True:
    for event in pygame.event.get():
        # check if the game is in new game mode, if so, display the new game menu
        game.new_game_menu(event, font)
        if game.check_win():
            # if check_win returns true, end the game and print out the winner
            text = font.render(f"Player {game.winner} wins!", True, setup.LINE_COLOR)
            screen.blit(text, (setup.WIDTH / 2 - text.get_width() / 2, text.get_height() / 2))
            game.game_over = True
        if game.is_board_full():
            # check if the game board is full, i.e. a draw
            game.game_over = True
        if event.type == pygame.QUIT:
            sys.exit()
        if game.single_player:
            # alternate between player 1 and player 2, since we are in single player mode
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.new_game:
                if game.player_turn == 1:
                    player1.make_move(game, screen)
                    game.change_turn()
                else:
                    player2.make_move(game, screen)
                    game.change_turn()

        if game.multi_player:
            # use computer player to make move as player 2
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.new_game:
                if game.player_turn == 1:
                    player1.make_move(game, screen)
                    game.change_turn()
                else:
                    com_player.make_move(game, screen)
                    game.change_turn()

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
