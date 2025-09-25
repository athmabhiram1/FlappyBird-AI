# FlappyBird-AI

An AI-powered version of the classic Flappy Bird game where a neural network learns to play using an enhanced genetic algorithm.  
Includes manual play, auto-training, and visualization with PyGame.

---

## 🚀 Features
- 🎮 **Manual Play** – Play Flappy Bird with simple controls  
- 🤖 **AI Training** – Train a neural network using a genetic algorithm  
- 🔁 **Enhanced Auto-Training** – Continuous sessions with detailed logging  
- 💾 **Model Saving/Loading** – Easily test trained AI models  
- 🖥️ **Visualization** – Watch AI evolve and learn in real-time  

---

## 📂 Project Structure
flappy_bird_ai/
│
├── game/
│ ├── init.py
│ ├── flappy_bird.py # Game logic
│ └── visualization.py # Enhanced PyGame display
│
├── ai/
│ ├── init.py
│ ├── neural_network.py # Neural network model
│ └── enhanced_genetic_algorithm.py # Enhanced training algorithm
│
├── models/ # Saved AI models
├── requirements.txt # Project dependencies
├── main.py # Main training script
├── auto_train.py # Enhanced auto-training script
├── start_training.bat # Windows batch script for easy training
└── test_components.py # Test suite

yaml
Copy code

---

## ⚙️ Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/FlappyBird-AI.git
cd FlappyBird-AI
pip install -r requirements.txt
Or install manually:

bash
Copy code
pip install pygame numpy torch
🎮 Usage
Manual Play
bash
Copy code
python game/flappy_bird.py
Controls:

SPACE → Flap wings

R → Restart after game over

Train AI
bash
Copy code
python main.py train
Enhanced Auto-Training
bash
Copy code
python auto_train.py train [generations]
python auto_train.py continuous [sessions]
Play with Trained AI
bash
Copy code
python main.py play models/final_best_model.pth
🧠 How It Works
Neural Network:

Input: Bird position, velocity, next pipe position (4 params)

Hidden: 2 layers, 16 neurons each

Output: Probability of flapping

Genetic Algorithm:

Population size: 20 (configurable)

Elite selection: Top 4 auto-advance

Tournament selection (size 5)

Weighted crossover for blending

Adaptive mutation for better exploration

🧪 Testing
Run the test suite:

bash
Copy code
python test_components.py
📜 License
This project is licensed under the MIT License.

pgsql
Copy code

👉 Just replace `your-username` with your actual GitHub username.  

Want me to also make a **fancy version with badges** (Python, PyGame, License, Stars, Forks, etc.) so it looks 
