import pygame
import sys
import os
import torch
import random
from game.flappy_bird import FlappyBirdGame, Bird, Pipe, PIPE_GAP
from ai.neural_network import NeuralNetwork
from ai.enhanced_genetic_algorithm import EnhancedGeneticAlgorithm as GeneticAlgorithm

# Ensure we can import from subdirectories
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def play_game_with_ai(network, render=False):
    """
    Play a game using the provided neural network
    Returns the score achieved
    """
    game = FlappyBirdGame()
    
    # If rendering, we need to handle events differently
    clock = None
    if render:
        game.screen = pygame.display.set_mode((400, 600))
        clock = pygame.time.Clock()
    
    while not game.game_over:
        # Get game state
        bird_y = game.bird.y / 600  # Normalize
        bird_velocity = game.bird.velocity / 10  # Normalize
        
        # Find the next pipe
        next_pipe = None
        for pipe in game.pipes:
            if pipe.x + 50 > game.bird.x:  # Pipe width is 50
                next_pipe = pipe
                break
        
        if next_pipe:
            pipe_x = next_pipe.x / 400  # Normalize
            pipe_gap_y = next_pipe.gap_y / 600  # Normalize
        else:
            pipe_x = 1.0
            pipe_gap_y = 0.5
        
        # Create state vector
        state = [bird_y, bird_velocity, pipe_x, pipe_gap_y]
        
        # Get AI decision
        flap_probability = network.predict(state)
        
        # Apply action based on probability
        if flap_probability > 0.5:
            game.bird.flap()
        
        # Update game
        game.update()
        
        # Render if requested
        if render and clock:
            game.draw()
            clock.tick(60)
            
            # Handle events for closing window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return game.score
    
    return game.score

def train_ai():
    """Train the AI using genetic algorithm"""
    print("Starting AI training...")
    
    # Create genetic algorithm
    ga = GeneticAlgorithm(population_size=20, mutation_rate=0.1, elite_size=4)
    
    # Training parameters
    generations = 50
    best_score = 0
    
    for generation in range(generations):
        print(f"Generation {generation + 1}/{generations}")
        
        # Evaluate each network in the population
        scores = []
        for i, network in enumerate(ga.population):
            score = play_game_with_ai(network)
            scores.append(score)
            print(f"  Network {i+1}: Score {score}")
        
        # Set fitness scores
        ga.set_fitness_scores(scores)
        
        # Track best score
        generation_best = max(scores)
        if generation_best > best_score:
            best_score = generation_best
            # Save the best network
            best_network = ga.get_best_network()
            model_path = os.path.join("models", f"best_model_gen_{generation+1}_score_{best_score}.pth")
            os.makedirs("models", exist_ok=True)
            best_network.save(model_path)
            print(f"  New best score: {best_score} - Model saved")
        
        # Evolve to next generation
        ga.evolve()
        
        print(f"  Generation best: {generation_best}")
        print(f"  Overall best: {best_score}")
        print()
    
    print("Training completed!")
    print(f"Best score achieved: {best_score}")
    
    # Save final best network
    final_best = ga.get_best_network()
    final_path = os.path.join("models", "final_best_model.pth")
    final_best.save(final_path)
    print(f"Final model saved to {final_path}")

def play_with_ai(model_path):
    """Play a game with a trained AI model"""
    print(f"Loading model from {model_path}")
    
    # Create network and load model
    network = NeuralNetwork()
    network.load(model_path)
    
    # Initialize pygame for rendering
    pygame.init()
    
    # Play game with rendering
    score = play_game_with_ai(network, render=True)
    print(f"Game ended with score: {score}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py train          - Train the AI")
        print("  python main.py train-auto     - Auto train the AI with enhanced logging")
        print("  python main.py play <model>   - Play with a trained model")
        return
    
    command = sys.argv[1]
    
    if command == "train":
        train_ai()
    elif command == "train-auto":
        # Enhanced auto training
        print("Starting enhanced auto training...")
        train_ai()  # For now, use the same function but you can replace with more advanced version
    elif command == "play":
        if len(sys.argv) < 3:
            print("Please specify model path")
            return
        model_path = sys.argv[2]
        play_with_ai(model_path)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()