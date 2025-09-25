"""
Auto-training script for Flappy Bird AI
This script provides enhanced automation for training the AI
"""

import pygame
import sys
import os
import torch
import random
import time
import json
from datetime import datetime
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

def auto_train_ai(
    generations=100,
    population_size=20,
    mutation_rate=0.2,
    elite_size=4,
    target_score=None,
    save_frequency=10,
    log_file="training_log.json"
):
    """
    Automatically train the AI with enhanced logging and control
    
    Args:
        generations: Number of generations to train
        population_size: Size of the population
        mutation_rate: Rate of mutation
        elite_size: Number of elite networks to keep
        target_score: Stop training if this score is reached (None for no limit)
        save_frequency: Save progress every N generations
        log_file: File to log training progress
    """
    print("Starting automatic AI training...")
    print(f"Parameters: generations={generations}, population={population_size}, mutation={mutation_rate}")
    
    # Create genetic algorithm
    ga = GeneticAlgorithm(population_size=population_size, mutation_rate=mutation_rate, elite_size=elite_size)
    
    # Training tracking
    best_score = 0
    best_network = None
    generation_times = []
    training_log = {
        "start_time": datetime.now().isoformat(),
        "parameters": {
            "generations": generations,
            "population_size": population_size,
            "mutation_rate": mutation_rate,
            "elite_size": elite_size
        },
        "generations": []
    }
    
    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)
    
    try:
        for generation in range(generations):
            gen_start_time = time.time()
            print(f"\nGeneration {generation + 1}/{generations}")
            
            # Evaluate each network in the population
            scores = []
            for i, network in enumerate(ga.population):
                score = play_game_with_ai(network)
                scores.append(score)
                print(f"  Network {i+1:2d}: Score {score:3d}")
            
            # Set fitness scores
            ga.set_fitness_scores(scores)
            
            # Track best score
            generation_best = max(scores)
            generation_avg = sum(scores) / len(scores)
            
            if generation_best > best_score:
                best_score = generation_best
                best_network = ga.get_best_network()
                # Save the best network
                model_path = os.path.join("models", f"best_model_gen_{generation+1}_score_{best_score}.pth")
                best_network.save(model_path)
                print(f"  🏆 New best score: {best_score} - Model saved")
            
            # Log generation data
            gen_data = {
                "generation": generation + 1,
                "best_score": generation_best,
                "average_score": generation_avg,
                "scores": scores,
                "time_taken": time.time() - gen_start_time
            }
            training_log["generations"].append(gen_data)
            
            # Save log file periodically
            if (generation + 1) % save_frequency == 0 or generation == generations - 1:
                with open(log_file, 'w') as f:
                    json.dump(training_log, f, indent=2)
                print(f"  📝 Progress logged to {log_file}")
            
            # Check if target score reached
            if target_score and best_score >= target_score:
                print(f"🎯 Target score {target_score} reached!")
                break
            
            # Evolve to next generation
            ga.evolve()
            
            gen_time = time.time() - gen_start_time
            generation_times.append(gen_time)
            
            print(f"  Generation best: {generation_best:3d} | Average: {generation_avg:5.1f} | Time: {gen_time:4.1f}s")
            print(f"  Overall best: {best_score:3d}")
        
        print("\n" + "="*50)
        print("Training completed!")
        print(f"Best score achieved: {best_score}")
        print(f"Average generation time: {sum(generation_times)/len(generation_times):.1f}s")
        
        # Save final best network
        if best_network:
            final_path = os.path.join("models", "final_best_model.pth")
            best_network.save(final_path)
            print(f"Final model saved to {final_path}")
        
        # Save final log
        training_log["end_time"] = datetime.now().isoformat()
        training_log["best_score"] = best_score
        with open(log_file, 'w') as f:
            json.dump(training_log, f, indent=2)
        print(f"Final training log saved to {log_file}")
        
        return best_network, best_score
        
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        if best_network and best_score > 0:
            interrupt_path = os.path.join("models", f"interrupted_model_score_{best_score}.pth")
            best_network.save(interrupt_path)
            print(f"Current best model saved to {interrupt_path}")
        return best_network, best_score

def continuous_training_session(
    sessions=5,
    generations_per_session=100,
    population_size=20,
    mutation_rate=0.2,
    elite_size=4
):
    """
    Run multiple training sessions continuously
    """
    print(f"Starting {sessions} continuous training sessions...")
    
    for session in range(sessions):
        print(f"\n{'='*60}")
        print(f"SESSION {session + 1}/{sessions}")
        print(f"{'='*60}")
        
        # Run training session
        best_network, best_score = auto_train_ai(
            generations=generations_per_session,
            population_size=population_size,
            mutation_rate=mutation_rate,
            elite_size=elite_size,
            log_file=f"training_log_session_{session+1}.json"
        )
        
        print(f"\nSession {session + 1} completed with best score: {best_score}")
        
        # Save session results
        session_result = {
            "session": session + 1,
            "best_score": best_score,
            "timestamp": datetime.now().isoformat()
        }
        
        session_file = f"session_{session+1}_result.json"
        with open(session_file, 'w') as f:
            json.dump(session_result, f, indent=2)
        print(f"Session results saved to {session_file}")
        
        if session < sessions - 1:
            print("Starting next session in 5 seconds...")
            time.sleep(5)

def main():
    """Main function with auto-training options"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python auto_train.py train [generations]          - Auto train AI")
        print("  python auto_train.py continuous [sessions]        - Run continuous training sessions")
        print("  python auto_train.py play <model>                 - Play with a trained model")
        return
    
    command = sys.argv[1]
    
    if command == "train":
        generations = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        auto_train_ai(generations=generations)
        
    elif command == "continuous":
        sessions = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        continuous_training_session(sessions=sessions)
        
    elif command == "play":
        if len(sys.argv) < 3:
            print("Please specify model path")
            return
        model_path = sys.argv[2]
        
        # Import play function from main
        from main import play_with_ai
        # Initialize pygame for rendering
        pygame.init()
        play_with_ai(model_path)
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()