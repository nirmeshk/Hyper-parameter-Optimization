from __future__ import print_function, division
from util import *
import random as r
from copy import deepcopy
import sys
from math import sqrt, exp, sin
import time
from sk import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import multiprocessing as mp
import matplotlib.animation as animation
from PIL import Image, ImageSequence
from images2gif import writeGif
import shutil
import os
import glob

r.seed(15)

class de():
    def __init__(self):
        self.settings = O(
            f = 0.75,
            max = 20,
            np = 50,
            cf = 0.3,
            epsilon = 0.01,
            me = 'de',)
        
    def optimize(self, model):
        print(self.__class__.__name__)
        population = [model.generate() for _ in range(self.settings.np)]
            
        frontier = []
        
        for can_1 in population:
            count = 1  # Number of candidates that can_1 dominates
            for can_2 in population:
                if model.cdom(can_1, can_2):
                    count += 1
            frontier.append((can_1, count))
        
        frontier = sorted(frontier, key = lambda (can, score): score)
        frontier = [ can for can, score in frontier]

        for _ in range(self.settings.max):
            self.update(frontier, model)
        
#         for can in frontier: print(can.decs)
        return frontier

    def update(self, frontier, model):
        for i, can in enumerate(frontier):
            new = self.extrapolate(frontier, model, can)
            if model.cdom(new, can):
                frontier[i] = new

        
    @staticmethod
    def threeOthers(frontier):
        two, three, four = r.sample(frontier, 3)
        
class ga():
    seed = 15678
    def __init__(self):
        self.settings = O(
        gens = 400,
        candidates = 500,
        better = lt,
        era = 100,
        retain = 0.33, #retain 33% of parents to next generation
        mutate_prob = 0.25
        )


    def optimize(self, model):

        ######   -- Log initial settings--  ######
        print(model)
        print("Settings: ")
        print(self.settings)
        #-----------------------------------------#


        #========================================#
        #### -- Initialize the Population -- #####
        #========================================#


        # Generate thrice the candidate size for the first time
        population = [model.generate(ga.seed) for _ in range(self.settings.candidates*3)]
        

        directory = model.__class__.__name__ + '/'
        if os.path.exists(directory): shutil.rmtree(directory); os.makedirs(directory)  
        else: os.makedirs(directory)  

        # Find out the scale for graphs
        obj_score = [model.eval(can) for can in population]
        f1_max = max([x[0] for x in obj_score])
        f2_max = max([x[1] for x in obj_score])
        f3_max = max([x[2] for x in obj_score])
        scale = (f1_max, f2_max, f3_max)

        ga.graph_it(population, model, scale)
        n = self.settings.candidates

        #=================================================#
        ######  Now the Evolution Begins    ###############
        #=================================================#

        for i in range(self.settings.gens):   
            print(i)
            # For the entire population, calculate its fitness score.
            # Fitness score is number of other can that a point dominates
            # After fitness calculation, retain x% of population as parents into next gen
            population = self.dominations(population, model)
            frontier = population[:int(n*0.30)]
            frontier += population[-int(n*0.10):] # For some variation

            # Add all the elite parents to next generation
            next_generation = frontier[:]

            while len(next_generation) < n:
                papa, mama = ga.select(frontier)
                new_can = ga.crossover(papa, mama, model)
                new_can = ga.mutate(new_can, model, self.settings.mutate_prob)
                if model.cdom(new_can, papa) or model.cdom(new_can, mama):
                    next_generation.append(new_can)
            print(len(population))
            population = next_generation[:] 
            
            if i == 0:
                baseline_population = deepcopy(population[:])
            
            ga.graph_it(population, model, scale)
            print('.')
            return baseline_population, population
  
    @staticmethod
    def dominations(population, model):
        """ 
            population: ith population
            model: the instance of model we are using
            retain: '%' of population to retain in next generation

            returns Sorted population according to its dominations
        """
        pop_dominations = []
        
        #Apply all pair continuous dominations
        for can_1 in population:
            dominated_by = 0  # Number of candidates that dominates can_1 
            for can_2 in population:
                if model.cdom(can_2, can_1):
                    dominated_by += 1
            pop_dominations.append((can_1, dominated_by))
        
        pop_dominations.sort(key = lambda (can, dominated_by): dominated_by)
        print([score for can, score in pop_dominations])  
        frontier = [can for (can, score) in pop_dominations]
        return frontier

    @staticmethod
    def select(elite_population):
        # Create a weighted roulette 
        # Each candidate will be added number of times its score
        roulette = elite_population[:]
        papa, mama = r.sample(roulette, 2)
        return (papa, mama)

    @staticmethod
    def crossover(papa, mama, model):
        pos = r.randint(0, len(papa.decs) - 1)
        can = papa.clone()
        can.decs[pos:] = mama.decs[pos:]
        return can

    @staticmethod
    def mutate(new_can, model, mutate_prob):
        # TODO: Any specific mutation method ??
        if r.random() < mutate_prob:
            for _ in range(int(len(new_can.decs)/4)):
                pos = r.randint(0, len(new_can.decs) - 1)
                new_can.decs[pos] = r.uniform(model.decs[pos].low, model.decs[pos].high)
        return new_can

    @staticmethod
    def graph_it(population, model, scale):
        final_frontier = [ model.eval(can) for can in population ]
        directory = model.__class__.__name__ + '/'
        file_name = directory + str(int(time.time()))

        # Plot results only if 2 or 3 dimensional
        if model.m == 2:
            # Plot results
            f1 = np.array([x[0] for x in final_frontier])
            f2 = np.array([x[1] for x in final_frontier])
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.scatter(f1, f2, color = '#ff5c33', alpha=0.7)
            ax.xlim([-100, 1000])
            ax.ylim([-100, 1000])
            ax.set_xlabel('f1')
            ax.set_ylabel('f2')
            fig.savefig(file_name)
        elif model.m == 3:
            # Plot results
            f1 = np.array([x[0] for x in final_frontier])
            f2 = np.array([x[1] for x in final_frontier])
            f3 = np.array([x[2] for x in final_frontier])
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(f1, f2, f3, s = 40, color = '#000080', alpha=0.80)
            ax.set_xlim((-100, scale[0]))
            ax.set_ylim((-100, scale[1]))
            ax.set_zlim((-100, scale[2]))
            ax.set_xlabel('f1')
            ax.set_ylabel('f2')
            ax.set_zlabel('f3')
            fig.savefig(file_name)


