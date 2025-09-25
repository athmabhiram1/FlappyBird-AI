# Flappy Bird AI

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://github.com/yourusername/flappy-bird-ai)

An implementation of the Flappy Bird game with an AI trained using genetic algorithms and neural networks. Watch as AI agents learn to navigate through pipes with increasing skill!

<p align="center">
  <img src="demo.gif" alt="Flappy Bird AI Demo" width="400"/>
</p>

## 🎮 Project Overview

This project combines the classic Flappy Bird game with artificial intelligence, allowing you to:
- Play the game manually
- Train an AI to play automatically
- Watch AI agents improve their performance over generations
- Experiment with different AI training parameters

The AI uses a neural network trained through a genetic algorithm to learn the optimal strategies for navigating through pipes without crashing.

## 📁 Project Structure

```
flappy_bird_ai/
│
├── game/
│   ├── __init__.py
│   ├── flappy_bird.py          # Core game logic and physics
│   └── visualization.py        # Enhanced PyGame graphics and display
│
├── ai/
│   ├── __init__.py
│   ├── neural_network.py             # Neural network implementation
│   └── enhanced_genetic_algorithm.py # Genetic algorithm for training
│
├── models/                     # Pre-trained AI models
├── requirements.txt            # Python dependencies
├── main.py                     # Main entry point for training
├── auto_train.py               # Advanced auto-training system
├── start_training.bat          # Windows training shortcut
└── test_components.py          # Test suite
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flappy-bird-ai.git
   cd flappy-bird-ai
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install packages individually:
   ```bash
   pip install pygame numpy torch
   ```

## ▶️ Usage

### Manual Play

Play the game yourself with keyboard controls:
```bash
python game/flappy_bird.py
```

**Controls:**
- **SPACEBAR** - Make the bird flap/jump
- **R** - Restart the game after game over

### AI Training

#### Basic Training
Train the AI from scratch:
```bash
python main.py train
```

#### Enhanced Auto-Training
For more advanced training with logging:
```bash
python main.py train-auto
```

#### Advanced Training Options
Train with custom parameters:
```bash
python auto_train.py train 200    # Train for 200 generations
python auto_train.py continuous 5 # Run 5 continuous training sessions
```

#### Windows Quick Start
On Windows, simply double-click `start_training.bat` to begin training with default parameters.

### Playing with Trained AI

Watch a pre-trained AI model play the game:
```bash
python main.py play models/final_best_model.pth
```

Or use the auto-train script:
```bash
python auto_train.py play models/final_best_model.pth
```

## 🧠 How It Works

### Game Mechanics

The Flappy Bird implementation follows the classic game rules:
- The bird is affected by gravity and falls continuously
- Players can make the bird flap upward to avoid pipes
- The game ends when the bird hits a pipe or the ground/ceiling
- Score increases for each pipe successfully navigated

### Neural Network Architecture

The AI uses a feedforward neural network with:
- **Input Layer**: 4 parameters
  - Bird's vertical position (normalized)
  - Bird's vertical velocity (normalized)
  - Next pipe's horizontal position (normalized)
  - Gap position of the next pipe (normalized)
- **Hidden Layers**: 2 hidden layers with 16 neurons each
- **Output Layer**: 1 neuron (probability of flapping)

### Genetic Algorithm

The training process uses an enhanced genetic algorithm:
- **Population**: 20 neural networks per generation
- **Selection**: Elite selection (top 4) + tournament selection
- **Crossover**: Weighted blending of parent networks
- **Mutation**: Adaptive mutation with configurable rates
- **Generations**: Evolves over many iterations to improve performance

## 📈 Performance

Our best AI models achieve impressive scores:
- **Top Score**: 501 points
- **Multiple models**: 100+ points
- **Early training**: 20-50 points after 50 generations
- **Extended training**: 100+ points after 200+ generations

## 🧪 Testing

Verify the project works correctly:
```bash
python test_components.py
```
<<<<<<< HEAD

This runs tests on all major components:
- Game logic
- Neural network
- Genetic algorithm
- Training scripts

## 🛠️ Customization

### Training Parameters

Modify training behavior by adjusting parameters in `auto_train.py`:
- `population_size`: Number of networks per generation
- `mutation_rate`: Probability of weight mutation
- `elite_size`: Number of top networks that survive unchanged
- `generations`: Number of training iterations

### Neural Network

Customize the neural network in `ai/neural_network.py`:
- Adjust hidden layer sizes
- Modify activation functions
- Change network architecture

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

Areas for improvement:
- Enhanced neural network architectures
- Improved genetic algorithm techniques
- Better visualization and graphics
- Additional game features
- Performance optimizations

## 🐛 Issues and Support

If you encounter any problems:
1. Check existing issues on GitHub
2. Create a new issue with detailed information
3. Include your system information and error messages

## 📧 Contact

- Project Link: [https://github.com/yourusername/flappy-bird-ai](https://github.com/yourusername/flappy-bird-ai)

## 🙏 Acknowledgments

- PyGame community for the game development library
- PyTorch for the neural network framework
- Inspiration from the original Flappy Bird game
