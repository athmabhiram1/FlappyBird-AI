import torch
import torch.nn as nn
import numpy as np

class NeuralNetwork(nn.Module):
    def __init__(self, input_size=4, hidden_size=16, output_size=1):
        super(NeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.network(x)
    
    def predict(self, state):
        """
        Predict whether to flap or not based on the current state
        state: [bird_y, bird_velocity, pipe_x, pipe_gap_y]
        Returns: probability of flapping (0-1)
        """
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            output = self.network(state_tensor)
            return output.item()
    
    def save(self, filepath):
        """Save the model to a file"""
        torch.save(self.state_dict(), filepath)
    
    def load(self, filepath):
        """Load the model from a file"""
        self.load_state_dict(torch.load(filepath))
        self.eval()

# Function to create the default neural network
def create_network():
    return NeuralNetwork()

if __name__ == "__main__":
    # Test the network
    net = create_network()
    test_input = [0.5, 0.1, 0.8, 0.6]  # Example state
    output = net.predict(test_input)
    print(f"Network output for test input: {output}")