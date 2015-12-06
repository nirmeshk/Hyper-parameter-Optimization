from copy import deepcopy
import random as r
from util import *
import math
from math import cos, sin, pi
from algorithms import *

class Decision():
    """ A wrapper class on decisions """
    def __init__(i, name, low, high):
        i.name = name
        i.low = low
        i.high = high


class Objective():
    """ A wrapper class on Objectives """
    def __init__(i, name, function, better=lt):
        i.name = str(name)
        i.function = function
        i.better = better

class Candidate(object):
    "A candidate decision values, objective scores, and energy"
    def __init__(self, decs = [], objs_score = [], energy = None):
        self.decs = decs
        self.objs_score = objs_score
        self.energy = energy

    def clone(self):
        new_can = Candidate()
        new_can.decs = deepcopy(self.decs)
        new_can.objs_score = self.objs_score[:]
        new_can.energy = self.energy
        return new_can

class Model(object):

    def __init__(i):
        i.decs = []
        i.objs = []

    def get_objs(i):
        return []

    def ok(i, can):
        return True

    def eval(i, can):
        return [obj.function(can) for obj in i.objs]

    def energy(i, can):
        can.objs_score = [obj.function(can) for obj in i.objs]
        return sum(can.objs_score)

    def __repr__(i):
        return str(zip(*i.decs)[0])

    def generate(i, r_ = r):
        """ Generates a candidate """
        count = 0
        while True:
            decs = [r_.uniform(d.low, d.high) for d in i.decs]
            one = Candidate(decs = decs)
            status = i.ok(one)
            count += 1
            if status:
                return one

    @staticmethod
    def exp_loss(x, y, n, better):
        loss = (x - y) if better == lt else (y - x)
        try:
            result = math.exp(loss / n)
        except:
            result = 10000000
        return result
    
    @staticmethod
    def total_loss(x, y, better):
        n = len(x)
        losses = [ Model.exp_loss(xi, yi ,n, better) for (xi, yi) in zip(x, y) ]
        return sum(losses) / n

    def cdom(i, can_1, can_2, better=lt):
       "x dominates y if it losses least"
       can_1.objs_score = [obj.function(can_1) for obj in i.objs]
       can_2.objs_score = [obj.function(can_2) for obj in i.objs]  
       x, y = can_1.objs_score, can_2.objs_score

       return True if Model.total_loss(x, y, better) < Model.total_loss(y, x, better) else False


    def bdom(i, can_1, can_2, better=lt):
        """
        Static method to check if one candidate dominates the other.
        :param can_1: List of points A
        :param can_2: List of points B
        :param better: greater/lesser function that used for domination
        """
        at_least = False

        can_1.objs_score = [obj.function(can_1) for obj in i.objs]
        can_2.objs_score = [obj.function(can_2) for obj in i.objs]

        for a, b in zip(can_1.objs_score, can_2.objs_score):
          if better(a,b):
            at_least = True
          elif a == b:
            continue
          else:
            return False
        return at_least

class GA_MODEL(Model):
    population = []
    population_model_instance = None
    
    def __init__(self, model_instance):
        """
            Args:
                model_instance: A model which this model will optimize.
        """
        
        self.n = 5
        self.m = model_instance.m      
        
        self.decs = [Decision(name="gens", low=200, high=600)]
        self.decs.append(Decision(name="era", low=50, high=200))
        self.decs.append(Decision(name="retain", low=0.1, high=0.5))
        self.decs.append(Decision(name="mutate_prob", low=0.25, high=0.75))
        self.decs.append(Decision(name="crossover_prob", low=0.65, high=0.99))         
        
        def f1(can):
            settings = O(
                gens = can.decs[0],
                candidates = 500,
                better = lt,
                era = can.decs[1],
                retain = can.decs[2],
                mutate_prob = can.decs[3],
                lives = 3,
                patience = 3,
                )
            ga_ = ga(settings)
            
            if len(GA_MODEL.population) == 0 or (len(GA_MODEL.population) > 0 and type(GA_MODEL.population_model_instance) != type(model_instance)):
                # From GA algorithm
                n = settings.candidates
                population = [model_instance.generate(r) for _ in range(n*3)]
                print('In GA model: after pop generated') 
                population = self.dominations(population, model_instance)
                print('In GA model: after pop generated') 
                frontier = population[:n]
                frontier += population[-n:] # For some variation
                r.shuffle(frontier)
                population = frontier[:n]

                GA_MODEL.population = population
                GA_MODEL.population_model_instance = model_instance

            baseline_population, population = ga_.optimize(model_instance, GA_MODEL.population)
            dist_from_hell = divergence_from_baseline(baseline_population, population, model_instance) 
            
            return dist_from_hell

        self.objs = [Objective(name = "f1", function = f1)]

    def generate(i, r_ = r):
        """ Generates a candidate """
        while True:
            decs = []
            for d in i.decs:
                if type(d.low) is int:
                    decs += [r_.randint(d.low, d.high)]
                else:
                    decs += [r_.uniform(d.low, d.high)]
            one = Candidate(decs = decs)
            if i.ok(one):
                return one

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

    
class DTLZ_1(Model):
    def __init__(self, n=10, m=2):
        """
            Args:
                n = number of decisions
                m = number of objectives
        """
        self.n = n
        self.m = m       
        self.decs = [Decision(name=d, low=0, high=1) for d in range(self.n)]
        self.objs = self.get_objs()

    def get_objs(self):
        # first m-1 objectives are same as respective decisions
        objectives = []

        def g(can):
            g_part_1 = 0
            for x in can.decs:
                g_part_1 += (x - 0.5)**2 - cos(20*pi*(x - 0.5)) 
            g = 100 * (len(can.decs) + g_part_1)
            return g

        def f0(can):
            f_ = 0.5 * (1 + g(can))
            for i in range(self.m - 1): f_ *= can.decs[i] 
            return f_

        objectives.append(Objective(name = 0, function = f0))

        for j in range(1, self.m - 1):
            def f(can):
                f_ = 0.5 * (1 + g(can))
                for k in range(self.m - (j+1)):
                    f_ *= can.decs[k]
                f_ *= 1 - can.decs[self.m - (j+1)]
                return f_
            objectives.append(Objective(name = j, function = f))

        def fm(can):
            return 0.5 *  (1 - can.decs[0]) * (1.0 + g(can))
        
        objectives.append(Objective(name = self.m-1, function = fm))   
        return objectives[:]

    def __repr__(self):
        s = ""
        s += "\nModel: {}".format(self.__class__.__name__)
        s += "\nArgs:"
        s += "\n\tnumber of decisions: {}".format(self.n)
        s += "\n\tnumber of objectives: {}".format(self.m)
        return s
    

class DTLZ_3(Model):
    def __init__(self, n=10, m=2):
        """
            Args:
                n = number of decisions
                m = number of objectives
        """
        self.n = n
        self.m = m       
        self.decs = [Decision(name=d, low=0, high=1) for d in range(self.n)]
        self.objs = self.get_objs()

    def get_objs(self):
        # first m-1 objectives are same as respective decisions
        objectives = []

        def g(can):
            g_part_1 = 0
            for x in can.decs:
                g_part_1 += (x - 0.5)**2 - cos(20*pi*(x - 0.5)) 
            g = 100 * (len(can.decs) + g_part_1)
            return g


        def f0(can):
            f_ = 0.5 * (1 + g(can))
            for i in range(self.m - 1): f_ *= cos(can.decs[i] * pi * 0.5)
            return f_
        objectives.append(Objective(name = 0, function = f0))

        for j in range(1, self.m - 1):
            def f(can):
                f_ = 0.5 * (1 + g(can))
                for k in range(self.m - (j+1)):
                    f_ *= cos(can.decs[k] * pi * 0.5)
                f_ *= sin( can.decs[self.m - (j+1)] * 0.5 )
                return f_
            objectives.append(Objective(name = j, function = f))

        def fm(can):
            return sin(can.decs[0] * pi * 0.5) * (1.0 + g(can))
        objectives.append(Objective(name = self.m-1, function = fm))
        
        return objectives[:]

    def __repr__(self):
        s = ""
        s += "\nModel: {}".format(self.__class__.__name__)
        s += "\nArgs:"
        s += "\n\tnumber of decisions: {}".format(self.n)
        s += "\n\tnumber of objectives: {}".format(self.m)
        return s



class DTLZ_5(Model):
    def __init__(self, n=10, m=2):
        """
            Args:
                n = number of decisions
                m = number of objectives
        """
        self.n = n
        self.m = m       
        self.decs = [Decision(name=d, low=0, high=1) for d in range(self.n)]
        self.objs = self.get_objs()

    def get_objs(self):
        objectives = []
        
        def g(can):
            g_ = 0
            for i in range(self.m):
                g_ += (can.decs[i] - 0.5)**2
            return g_

        def theta(can, i):
            x = pi * (1 + 2 * g(can) * can.decs[i]) / (4 * (1 + g(can)))
            return x

        def f0(can):
            f_ = (1 + g(can))
            for x in range(self.m - 1):
                f_ *= cos( theta(can, x) * pi * 0.5)
            return f_

        objectives.append(Objective(name = 0, function = f0))

        for j in range(1, self.m - 1):
            def f(can):
                f_ = 0.5 * (1 + g(can))
                for k in range(self.m - (j+1)):
                    f_ *= cos(theta(can, k) * pi * 0.5)
                f_ *= sin( theta(can, self.m - (j+1)) * 0.5 )
                return f_
            objectives.append(Objective(name = j, function = f))

        def fm(can):
            return sin(theta(can, 0) * pi * 0.5) * (1.0 + g(can))

        objectives.append(Objective(name = self.m-1, function = fm))
        return objectives[:]

    def __repr__(self):
        s = ""
        s += "\nModel: {}".format(self.__class__.__name__)
        s += "\nArgs:"
        s += "\n\tnumber of decisions: {}".format(self.n)
        s += "\n\tnumber of objectives: {}".format(self.m)
        return s


class DTLZ_7(Model):
    def __init__(i, n=10, m=3):
        """
            Args:
                n = number of decisions
                m = number of objectives
        """
        i.n = n
        i.m = m       
        i.decs = [Decision(name=d, low=0, high=1) for d in range(i.n)]
        i.objs = i.get_objs()

    def get_objs(i):
        # first m-1 objectives are same as respective decisions
        objectives = []
        for j in range(i.m - 1):
            def f(can):
                return can.decs[0]
            objectives.append(Objective(name = j, function = f))

        def g(can):
            g = 1 + 9.0 / len(can.decs) * sum(can.decs)
            return g
        
        def fm(can):
            summation = 0.0
            for j in range(i.m - 1):
                f_i = can.decs[j]
                summation += (f_i / (1 + g(can))) * (1 + sin(3 * pi * f_i))
            h = (i.m - summation)
            return (1 + g(can)) * h

        objectives.append(Objective(name = i.m-1, function = fm))
        return objectives[:]
    
    def __repr__(self):
        s = ""
        s += "\nModel: {}".format(self.__class__.__name__)
        s += "\nArgs:"
        s += "\n\tnumber of decisions: {}".format(self.n)
        s += "\n\tnumber of objectives: {}".format(self.m)
        return s

if __name__ == '__main__':
    a = DTLZ_3(5, 4)
    print(a)
