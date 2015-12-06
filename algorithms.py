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
import shutil
import os
import glob

class de():
    def __init__(self):
        self.settings = O(
            f = 0.75,
            max = 10,
            np = 5,
            cf = 0.3,
            epsilon = 0.01,
            me = 'de',)
        
    def optimize(self, model):
        print(self.__class__.__name__)
        r.seed(15)
        population = [model.generate(r) for _ in range(self.settings.np)]
            
        baseline_population = deepcopy(population[:])

#         for can in baseline_population: print(can.decs)

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
        return baseline_population, frontier

    def update(self, frontier, model):
        for i, can in enumerate(frontier):
            new = self.extrapolate(frontier, model, can)
            if model.cdom(new, can):
                frontier[i] = new

        
    @staticmethod
    def threeOthers(frontier):
        two, three, four = r.sample(frontier, 3)
        return two, three, four
    
    def extrapolate(self, frontier, model, one):
        new = one.clone()
    
        for _ in range(5):
            two, three, four = de.threeOthers(frontier)
            c = r.randint(0, len(new.decs) - 1)
                    
            for j in range(len(new.decs)):
                if r.random() < self.settings.cf or j == c:
                    new.decs[j] = two.decs[j] + self.settings.f * (three.decs[j] - four.decs[j])
                    if type(model.decs[j].low) is int:
                        new.decs[j] = int(new.decs[j])

            
            if model.ok(new):
                break
            
        if model.ok(new):
            return new
        
        return one
        
class ga():
    def __init__(self, setting = O(
            gens = 500,
            candidates = 500,
            better = lt,
            era = 100,
            retain = 0.33, #retain 33% of parents to next generation
            mutate_prob = 0.25,
            lives = 3,
            patience = 3
            ), visualize = False, fp = None):
        self.settings = setting
        self.visualize = visualize
        self.fp = fp
        
    def optimize(self, model, population = None):

        ######   -- Log initial settings--  ######
        print(model)
        print("Settings: ")
        print(self.settings)

        if self.fp:
            self.fp.write(str(model))
            self.fp.write("\nSettings: \n")
            self.fp.write(str(self.settings))

        
        #-----------------------------------------#
        
        #========================================#
        #### -- Initialize the Population -- #####
        #========================================#


        print('before start') 
        # Generate thrice the candidate size for the first time
        n = self.settings.candidates
        if population is None:
            n = self.settings.candidates
            population = [model.generate(r) for _ in range(n*3)]
            print('after pop generated') 
            population = self.dominations(population, model)
            print('after pop generated') 
            frontier = population[:n]
            frontier += population[-n:] # For some variation
            r.shuffle(frontier)
            population = frontier[:n]
        
        baseline_population = deepcopy(population[:])
        cur_era = prev_era = deepcopy(population[:])
        
        print('start') 
        #=================================#
        ###  Visualization Code        ####
        #=================================#
        if self.visualize:
            # Create a directory and remove the old one.
            directory = model.__class__.__name__ + '/'
            if os.path.exists(directory): shutil.rmtree(directory); os.makedirs(directory)  
            else: os.makedirs(directory)

            # Find out the scale for graphs
            obj_score = [model.eval(can) for can in population]
            f1_max = max([x[0] for x in obj_score])
            f2_max = max([x[1] for x in obj_score])
            f3_max = max([x[2] for x in obj_score])
            scale = (f1_max*1.1, f2_max*1.1, f3_max*1.1)
            ga.graph_it(population, model, scale)

        #=================================================#
        ######  Now the Evolution Begins    ###############
        #=================================================#

        
        print('-')
        for i in range(self.settings.gens):   
            print('-')
            # For the entire population, calculate its fitness score.
            # Fitness score is number of other can that a point dominates
            # After fitness calculation, retain x% of population as parents into next gen
            population = self.dominations(population, model)

            # Retain self.settings.retain % elite parents
            to_retain = n*self.settings.retain
            if int(to_retain) is 0:
                to_retain = 1
            frontier = population[:int(to_retain)]

            # For some variation, retain some bad candidates
            to_retain = to_retain * 0.5
            if int(to_retain) is 0:
                to_retain = 1
            frontier += population[-int(n*self.settings.retain*0.5):] 

            # Safety check if frontier goes above n.
            if len(frontier) > n:
                frontier = frontier[:n]
            
            # Add all the elite parents to next generation
            next_generation = frontier[:]

            while len(next_generation) < n:
                papa, mama = ga.select(frontier)
                new_can = ga.crossover(papa, mama, model)
                new_can = ga.mutate(new_can, model, self.settings.mutate_prob)
                if model.cdom(new_can, papa) or model.cdom(new_can, mama):
                    next_generation.append(new_can)
            
            population = next_generation[:] 

            # Check for early termination
            if i != 0 and i % self.settings.era == 0:
                print('\n')
                prev_era = cur_era
                cur_era = population
                if earlyTermination(prev_era, cur_era, model):
                    self.settings.patience -= 1
                    print('Patience = ', self.settings.patience)
                    if self.settings.patience == 0:
                        print ('Early Termination at ', str(int(i/self.settings.era)))
                        if self.fp: self.fp.write('Early Termination at {}\n'.format(int(i%self.settings.era)))
                        break
                else:
                    self.settings.patience = self.settings.lives

            if self.visualize: ga.graph_it(population, model, scale)


        return baseline_population, population
  
    @staticmethod
    def dominations(population, model):
        """ 
        Args:
            population: ith population
            model: the instance of model we are using
            returns Sorted population according to its domination scores
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
            ax.xlim([0, 1000])
            ax.ylim([0, 1000])
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
            ax.set_xlim((0, scale[0]))
            ax.set_ylim((0, scale[1]))
            ax.set_zlim((0, scale[2]))
            ax.set_xlabel('f1')
            ax.set_ylabel('f2')
            ax.set_zlabel('f3')
            fig.savefig(file_name)
