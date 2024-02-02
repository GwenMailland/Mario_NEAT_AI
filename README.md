# Mario_NEAT_AI


The provided Python script implements a genetic algorithm using the NEAT (NeuroEvolution of Augmenting Topologies) library to evolve neural networks for playing the Super Mario Bros game. The algorithm evaluates the fitness of individual genomes (neural networks) based on Mario's progress in the game.

#### Key Components:

1. NEAT Configuration:
   - Configures the NEAT algorithm with parameters for genome evolution, reproduction, species set, and stagnation.

2. Worker Class:
   - Defines a `Worker` class responsible for evaluating the fitness of individual genomes.
   - Initializes a Super Mario Bros environment and uses a NEAT-created neural network to control Mario's actions.
   - Converts game observations to grayscale, resizes them, and flattens the resulting image for input to the neural network.
   - Evaluates the fitness based on Mario's progress, handling termination conditions such as reaching the flag or losing a life.

3. Evaluation Function (`eval_genomes`):
   - Takes a genome and NEAT configuration as input.
   - Creates an instance of the `Worker` class to evaluate the fitness of the genome in the Super Mario Bros environment.

4. NEAT Population Initialization:
   - Initializes a NEAT population and adds reporters for monitoring progress and saving checkpoints.

5. Parallel Evaluation:
   - Utilizes NEAT's `ParallelEvaluator` to evaluate genomes in parallel, improving performance.

6. Visualization and Saving:
   - Visualizes and saves statistics, species information, and neural network structures during the evolution process.
   - Saves the winning genome and associated neural network for future use.

7. Visualization of Evolution Results:
   - Generates visualizations of the evolution process, including fitness over generations and the species distribution.
