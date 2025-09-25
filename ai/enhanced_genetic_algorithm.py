import numpy as np
import random
import torch
from ai.neural_network import NeuralNetwork

class EnhancedGeneticAlgorithm:
    def __init__(self, population_size=20, mutation_rate=0.2, elite_size=4, 
                 mutation_strength=0.3, tournament_size=5, adaptive_mutation=True):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.adaptive_mutation = adaptive_mutation
        self.population = []
        self.fitness_scores = []
        self.generation = 0
        
        # Initialize population
        self.initialize_population()
    
    def initialize_population(self):
        """Create initial population of neural networks"""
        self.population = []
        for _ in range(self.population_size):
            network = NeuralNetwork()
            self.population.append(network)
    
    def select_parents(self):
        """Select parents using tournament selection"""
        # Combine population and fitness scores
        combined = list(zip(self.population, self.fitness_scores))
        # Sort by fitness (descending)
        combined.sort(key=lambda x: x[1], reverse=True)
        
        # Select elite members
        elite = [network for network, _ in combined[:self.elite_size]]
        
        # Select remaining parents through tournament selection
        parents = elite.copy()
        while len(parents) < self.population_size:
            # Tournament selection with larger tournament size for better selection pressure
            tournament = random.sample(combined, min(self.tournament_size, len(combined)))
            winner = max(tournament, key=lambda x: x[1])
            parents.append(winner[0])
        
        return parents
    
    def crossover(self, parent1, parent2):
        """Create a child network by combining weights from two parents"""
        child = NeuralNetwork()
        
        # Get state dictionaries
        parent1_dict = parent1.state_dict()
        parent2_dict = parent2.state_dict()
        child_dict = child.state_dict()
        
        # For each parameter, combine parents with weighted average
        for key in child_dict:
            # Blend weights from both parents
            alpha = random.uniform(0.3, 0.7)  # Weighted blend rather than binary choice
            child_dict[key] = alpha * parent1_dict[key] + (1 - alpha) * parent2_dict[key]
        
        child.load_state_dict(child_dict)
        return child
    
    def mutate(self, network):
        """Apply random mutations to a network with adaptive strength"""
        with torch.no_grad():
            for param in network.parameters():
                if len(param.shape) > 1:  # Weight matrices
                    mutation_mask = torch.rand(param.shape) < self.mutation_rate
                    noise = torch.randn(param.shape) * self.mutation_strength
                    param += mutation_mask * noise
                else:  # Bias vectors
                    mutation_mask = torch.rand(param.shape) < self.mutation_rate
                    noise = torch.randn(param.shape) * self.mutation_strength
                    param += mutation_mask * noise
    
    def evolve(self):
        """Create the next generation"""
        self.generation += 1
        
        # Adaptive mutation - increase mutation rate if no improvement
        if self.adaptive_mutation and len(self.fitness_scores) > 0:
            current_best = max(self.fitness_scores)
            # If we have history, check for stagnation
            if hasattr(self, 'previous_best') and self.previous_best == current_best:
                self.stagnation_counter = getattr(self, 'stagnation_counter', 0) + 1
                if self.stagnation_counter > 5:  # If stuck for 5 generations
                    # Increase mutation rate to escape local optima
                    self.mutation_rate = min(self.mutation_rate * 1.2, 0.5)
                    self.mutation_strength = min(self.mutation_strength * 1.1, 0.5)
                    print(f"  🔧 Adaptive mutation: rate={self.mutation_rate:.3f}, strength={self.mutation_strength:.3f}")
            else:
                self.stagnation_counter = 0
                # Gradually decrease mutation rate for fine-tuning
                self.mutation_rate = max(self.mutation_rate * 0.95, 0.05)
                self.mutation_strength = max(self.mutation_strength * 0.95, 0.05)
            
            self.previous_best = current_best
        
        # Select parents
        parents = self.select_parents()
        
        # Create new population
        new_population = []
        
        # Keep elite members (no mutation for elite)
        for i in range(self.elite_size):
            new_population.append(parents[i])
        
        # Create children through crossover and mutation
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        
        self.population = new_population
        self.fitness_scores = [0] * self.population_size  # Reset fitness scores
    
    def get_best_network(self):
        """Return the best network from the current population"""
        if not self.fitness_scores:
            return self.population[0]
        
        best_index = np.argmax(self.fitness_scores)
        return self.population[best_index]
    
    def set_fitness_scores(self, scores):
        """Set fitness scores for the current population"""
        self.fitness_scores = scores

# Example usage
if __name__ == "__main__":
    ga = EnhancedGeneticAlgorithm()
    print(f"Initialized population of {len(ga.population)} networks")
    
    # Example of running one generation
    # In practice, you would evaluate each network by playing games
    dummy_scores = [random.randint(0, 100) for _ in range(ga.population_size)]
    ga.set_fitness_scores(dummy_scores)
    
    print(f"Best score: {max(dummy_scores)}")
    
    # Evolve to next generation
    ga.evolve()
    print("Evolved to next generation")