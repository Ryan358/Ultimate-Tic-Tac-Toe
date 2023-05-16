from tictactoenn import DQN
import torch
# Initialize the DQN

loaded_dict_state = torch.load("dqn.pth")
tictactoe_ai = DQN()
tictactoe_ai.load_state_dict(loaded_dict_state)

tictactoe_ai.eval()

sample_board = torch.tensor([[1, 2, 2], [0, 0, 0], [0, 0, 0]], dtype=torch.float32).unsqueeze(0).unsqueeze(0)
with torch.no_grad():
    output = tictactoe_ai(sample_board)
    action_space = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    discretized_output = action_space[torch.argmax(output)]
    print(output)

