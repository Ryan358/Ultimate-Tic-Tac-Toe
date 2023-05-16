"""This code declares and trains a DQN model to play tic-tac-toe. The model is trained by playing games against another
computer player. The model is trained to predict the best move to make given a board state (3x3 array) and outputs the
ideal move as an ordered pair. The model is trained using a replay buffer, which stores the last 1000 board states and
the corresponding moves. The model is trained by randomly sampling 32 board states from the replay buffer."""
import random
import game_setup as setup
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim




class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=1, stride=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 64, kernel_size=1, stride=1)
        self.relu2 = nn.ReLU()
        self.fc1 = nn.Linear(64 * 3 * 3, 128)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, 2)  # 2 for x and y coordinates of the action

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x

    def predict(self, state):
        with torch.no_grad():
            action = self.forward(state)

            # convert to numpy array
            action = action.numpy()
            # convert to row, column integers
            action = divmod(action, 3)
            return action

def main():
    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    else:
        device = torch.device('cpu')
    print(f"Using device: {device}")
    # Hyperparameters
    EPSILON_INITIAL = 0.9
    EPSILON_FINAL = 0.1
    EPSILON_DECAY = 0.999
    REPLAY_MEMORY_CAPACITY = 10000
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    DISCOUNT_FACTOR = 0.99
    TRAINING_ITERATIONS = 1000

    # Initialize the DQN
    dqn = DQN()
    dqn.to(device)
    optimizer = optim.Adam(dqn.parameters(), lr=LEARNING_RATE)
    mse_loss = nn.MSELoss()

    # Replay memory buffer
    replay_memory = []

    # Exploration-exploitation strategy
    epsilon = EPSILON_INITIAL

    # Initialize the game
    player1 = setup.ComputerPlayer(1, True)
    player2 = setup.ComputerPlayer(2, True)
    game = setup.Game(graphics_enabled=False)

    for iteration in range(TRAINING_ITERATIONS):
        game.reset_game()
        game_over = False
        state = np.copy(game.board)
        while not game_over:
            if game.player_turn == 1:
                if random.random() < epsilon:
                    if not game.is_board_full():
                        action = player1.make_move(game, None)
                        next_state = np.copy(game.board)

                else:
                    # Use the DQN to predict the best move.
                    if not game.is_board_full():
                        q_values = dqn(torch.tensor(state, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device))
                        action = torch.argmax(q_values).item()
                        action = divmod(action, 3)
                        game.mark_square(action[0], action[1], 1)
                        next_state = np.copy(game.board)
            else:
                if random.random() < epsilon:
                    if not game.is_board_full():
                        action = player2.make_move(game, None)
                        next_state = np.copy(game.board)
                    else:
                        q_values = dqn(torch.tensor(state, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device))
                        action = torch.argmax(q_values).item()
                        action = divmod(action, 3)
                        game.mark_square(action[0], action[1], 2)
                        next_state = np.copy(game.board)
            game.change_turn()

            reward = 0.0

            if game.check_win() and game.winner == 1:
                reward = 1.0
                game_over = True
            elif game.check_win() and game.winner == 2:
                reward = -1.0
                game_over = True
            elif game.is_board_full() and not game.check_win():
                reward = 0.5
                game_over = True
            else:
                reward = 0.0
            if game.is_board_full():
                game_over = True
            # Add the state and action to the replay memory
            replay_memory.append((state, action, reward, next_state, game_over))
            state = next_state.copy()

            epsilon = max(EPSILON_FINAL, epsilon * EPSILON_DECAY)
            if len(replay_memory) >= BATCH_SIZE:
                batch = random.sample(replay_memory, BATCH_SIZE)
                states, actions, rewards, next_states, game_overs = zip(*batch)

                states = torch.tensor(states, dtype=torch.float32).unsqueeze(1).to(device)
                actions = torch.tensor(actions, dtype=torch.long).to(device)
                rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
                next_states = torch.tensor(next_states, dtype=torch.float32).unsqueeze(1).to(device)
                game_overs = torch.tensor(game_overs, dtype=torch.float32).to(device)

                q_values = dqn(states).squeeze(1)
                action_indices = actions[:, 0] * 3 + actions[:, 1]
                q_values_selected = q_values.gather(0, action_indices.unsqueeze(1))

                target_q_values = rewards + DISCOUNT_FACTOR * torch.max(dqn(next_states), dim=1)[0] * (1 - game_overs)
                target_q_values = target_q_values.squeeze()

                loss = mse_loss(q_values_selected.squeeze(1), target_q_values)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                print(f"Iteration: {iteration} out of {TRAINING_ITERATIONS}, Loss: {loss.item()}")

    torch.save(dqn.state_dict(), 'dqn.pth')


if __name__ == '__main__':
    main()
