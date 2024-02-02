from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import gym
from matplotlib import pyplot as plt
from gym.wrappers import GrayScaleObservation
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
import numpy as np
import neat
import pickle
import cv2
import visualize
import csv
import multiprocessing




class Worker(object):

    def __init__(self, genome, config):
        self.genome = genome
        self.config = config
        
    def work(self):

        self.env = gym.make('SuperMarioBros-v2', apply_api_compatibility=True)
        self.env = JoypadSpace(self.env, SIMPLE_MOVEMENT)

        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

        done = False
        obs,info= self.env.reset()
        i=0
        fitness=0
        fitness_max=41
        genome_fitness=0

        while done==False:
            
            
             #RuntimeError: Expected 1120 inputs, got 61440
            obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(obs, (28, 40))

            # Aplatir l'image résultante
            screen = np.ndarray.flatten(screen)



            output = net.activate(screen)
            output=output.index(max(output))
            
            obs, reward, terminated, truncated, info = self.env.step(output)

            done = terminated or truncated
            fitness=info["x_pos"]
            if fitness>fitness_max:
                i=0
                fitness_max=fitness
            else:
                i+=1
            
            if done or i>200 or info["life"]<2:
                done=True

                genome_fitness=int(fitness_max)
                return genome_fitness

            if info["flag_get"]==True:
                done=True
                genome_fitness=110000
                
            
                return genome_fitness
            
            
        
def eval_genomes(genome, config):
    
    worky = Worker(genome, config)
    return worky.work()







if __name__ == '__main__':

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'config-feedforward')


    #pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-399')
    pop = neat.Population(config)

  

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(50))


    pe = neat.ParallelEvaluator(multiprocessing.cpu_count()-1, eval_genomes)

    #winner=pop.run(eval_genomes, 2)
    winner = pop.run(pe.evaluate)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    with open("winner-feedforwars","wb") as filename:
        pickle.dump(winner,filename)

    #node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", prune_unused=True)