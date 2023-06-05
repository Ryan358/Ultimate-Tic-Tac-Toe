"""This code tests the  model by playing games against another computer player. The model is tested by playing 100
games"""
import numpy as np
from tabular_q import QTable, QAgent, convert_to_grid
import game_setup as setup


def main():
    # play a game against another Q-agent
    game = setup.Game(setup.start_game(), False)
    q_table = QTable()
    q_table.load("qtable.csv")
    agent1 = QAgent(game, 1, q_table=q_table, epsilon=0)
    agent2 = QAgent(game, 2, q_table=q_table, epsilon=0)
    # play 100 games without learning or updating the Q-table
    num_games = 1000
    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    for i in range(num_games):
        game.reset_game()
        while not game.check_win() and not game.is_board_full():
            # get the current player's turn
            player = game.player_turn
            # get the action for the current player
            action = agent1.make_move() if game.player_turn == agent1.player_num else agent2.make_move()
            # make the move
            move = convert_to_grid(action)
            game.mark_square(move[0], move[1], player)
            # change the turn
            game.change_turn()
        # check who won
        if game.check_win():
            if game.winner == 1:
                agent1_wins += 1
            else:
                agent2_wins += 1
        else:
            draws += 1

    print("Agent 1 wins: ", agent1_wins)
    print("Agent 2 wins: ", agent2_wins)
    print("Draws: ", draws)









if __name__ == '__main__':
    main()
