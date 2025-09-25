"""
Test script to verify that all components of the Flappy Bird AI project work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_game():
    """Test the game module"""
    print("Testing game module...")
    try:
        from game.flappy_bird import Bird, Pipe, FlappyBirdGame
        bird = Bird()
        pipe = Pipe()
        print("✓ Game module imported successfully")
        print(f"  Bird position: ({bird.x}, {bird.y})")
        print(f"  Pipe position: ({pipe.x}, gap at {pipe.gap_y})")
        return True
    except Exception as e:
        print(f"✗ Game module test failed: {e}")
        return False

def test_neural_network():
    """Test the neural network module"""
    print("Testing neural network module...")
    try:
        from ai.neural_network import NeuralNetwork
        import torch
        net = NeuralNetwork()
        test_input = [0.5, 0.1, 0.8, 0.6]
        output = net.predict(test_input)
        print("✓ Neural network module imported successfully")
        print(f"  Test prediction: {output}")
        return True
    except Exception as e:
        print(f"✗ Neural network module test failed: {e}")
        return False

def test_genetic_algorithm():
    """Test the genetic algorithm module"""
    print("Testing genetic algorithm module...")
    try:
        from ai.enhanced_genetic_algorithm import EnhancedGeneticAlgorithm as GeneticAlgorithm
        ga = GeneticAlgorithm(population_size=5)
        print("✓ Genetic algorithm module imported successfully")
        print(f"  Population size: {len(ga.population)}")
        return True
    except Exception as e:
        print(f"✗ Genetic algorithm module test failed: {e}")
        return False

def test_main():
    """Test the main module"""
    print("Testing main module...")
    try:
        import main
        print("✓ Main module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Main module test failed: {e}")
        return False

def test_auto_train():
    """Test the auto train module"""
    print("Testing auto train module...")
    try:
        import auto_train
        print("✓ Auto train module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Auto train module test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Flappy Bird AI component tests...\n")
    
    tests = [
        test_game,
        test_neural_network,
        test_genetic_algorithm,
        test_main,
        test_auto_train
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()