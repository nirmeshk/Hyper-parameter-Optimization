#### Contributors:
- Nirmesh Khandelwal
- Anand Bora
- Ravi Singh

#### Abstract
- As a part of this experiment, we used Differential Evolution (DE) to tune default "magic" parameters for Genetic Algorithms (GA).

#### Overview and Design Considerations:
- We used DE algorithm with following default settings: 
```
  Settings: 
    { 
      f = 0.75,         # extrapolate amount
      max = 50,         # number of repeats 
      np = 10,          # number of candidates
      cf = 0.3,         # prob of cross-over 
      epsilon = 0.01,
    }
```
- In order to optimize the GA algorithm, we created a GA model with four decisions and one objective 
  - Four decisions of GA model are the magic parameters of GA algorithm to be tuned.
```
        Decision(name="gens", low=200, high=600)
        Decision(name="era", low=50, high=200)
        Decision(name="retain", low=0.1, high=0.5)
        Decision(name="mutate_prob", low=0.25, high=0.75)
```
- Single objective function of GA model, initializes an instance of GA algorithm with the decisions and passes the actual model we intend to optimize to GA algorithm. GA algorithm returns returns the final population. The objective function returns the "divergence distance" of the final population with the baseline population.  
- Note that all instances of GA algorithm are optimized with the same baseline population.
- At the end of the runs of DE, we get a frontier of tuned GAs. To compare it with untuned GA, we choose an untuned GA with magic parameters as the mean of individual decisions. Example: "gens" have low and high of 200 and 600 respectively, and untuned GA had "gens" set to 400.  

### GA Algorithm implementation
Here is what we did:

- Generate a random population in the start.
- Sort the entire population based on their domination scores in increasing order. A domination score of candidate 'a' is number of other candidates that dominate 'a'.
- Choose first x% and last y% from the sorted population to be parents for next generation. 
- Produce `total_population_size - len(parents)` new children by select , crossover and mutate among parents. 
- parents + new children contitute next generation.

- Here is the basic code for the implementation (Just for explanation purpose):
```python
def GA(model):
	population = [model.generate() for _ in pop_size]
	
	for _ in range(number_of_gen):
		population.sort(key = lambda can: can.domination_score)
		parents = population[:x] + population[-y:]        # Keep top x% and bottom y%
		next_gen = parents[:]

		while len(next_gen)  < len(population):
			papa, mama = select(parents)
			son = crossover(papa, mama)
			son = mutate(son)
			next_gen.append(son)

		population = next_gen[:]
```

### Challenges:
- Slow performance of GA
- Used some form of memmoization to speedup things little bit. And it helped!!
  - Normally when we optimize a model, we do not care about "caching" objective scores as objecitve scores were some sort of mathematical function of decisions, and fairly fast calculations. But in this case, objective function of GA model calls an instance of GA algorithm and "caching" these values saved a lot of time. 
- Difficult to debug even small mistakes: seed of random, keeping same baseline population for all ga optimized by DE.
- A good objective score to measure for 1) Early termination 2) Comparing different GA optimizers.
- Even tried some easy models, but those models lack interesing results as they are easily optimized in very few generations. Also, the GA code n*n was the main culprit after we did some profiling.

### Results:
We observed that tuned GAs performed better than untuned GA.
We ran it for DTLZ1 (2 objectives and 5 decisions) and for GA algorithm for 80 and 200 candidate sizes.

##### Small (80 GA candidates, DTLZ1 - 2 Objectives, 5 Decisions)

| Rank | Tuned / Untuned | Final Divergence | Settings |
|-------------|-------------|-------------|------------------|
| 1  | tuned | 56.09 | { gens = 398, era = 71 , retain = 0.46, mutate_prob = 0.57 }  |
| 2  | tuned | 55.44 | { gens = 454, era = 80 , retain = 0.45, mutate_prob = 0.44 }  |
| 3  | tuned | 54.63 | { gens = 404, era = 197, retain = 0.42, mutate_prob = 0.43 }  |
| 4  | tuned | 52.83 | { gens = 587, era = 51 , retain = 0.39, mutate_prob = 0.42 }  |
| 5  | tuned | 50.57 | { gens = 292, era = 173, retain = 0.27, mutate_prob = 0.41 }  |
| 6  | tuned | 49.22 | { gens = 206, era = 143, retain = 0.38, mutate_prob = 0.39 }  |
| 7  | tuned | 47.92 | { gens = 476, era = 77 , retain = 0.38, mutate_prob = 0.49 }  |
| 8  | tuned | 45.92 | { gens = 386, era = 157, retain = 0.34, mutate_prob = 0.67 }  |
| 9  | tuned | 44.58 | { gens = 231, era = 135, retain = 0.26, mutate_prob = 0.36 }  |
| 10 | tuned | 42.23 | { gens = 570, era = 186, retain = 0.27, mutate_prob = 0.34 }  |
| 11 | **un-tuned** | 35.97 | { gens = 400, era = 125, retain = 0.44, mutate_prob = 0.64 } |

##### Large (200 GA candidates, DTLZ1 - 2 Objectives, 5 Decisions)
| Rank | Tuned / Untuned | Final Divergence | Settings |
|-------------|-------------|-------------|------------------|
| 1  | tuned | 35.48 | { gens = 291, era = 179, retain = 0.44, mutate_prob = 0.64 } |
| 2 | **un-tuned** | 34.31 | { gens = 400, era = 125, retain = 0.44, mutate_prob = 0.64 } |
| 3  | tuned | 31.79 | { gens = 356, era = 72, retain = 0.37, mutate_prob = 0.57 } |
| 4  | tuned | 31.78 | { gens = 334, era = 73, retain = 0.45, mutate_prob = 0.50 } |
| 5  | tuned | 31.65 | { gens = 457, era = 156, retain = 0.49, mutate_prob = 0.39 } |
| 6  | tuned | 28.11 | { gens = 240,era = 67, retain = 0.49, mutate_prob = 0.48 } |
| 7  | tuned | 27.32 | { gens = 441, era = 98, retain = 0.49, mutate_prob = 0.62 } |
| 8  | tuned | 24.10 | { gens = 503, era = 114, retain = 0.23, mutate_prob = 0.39 } |
| 9  | tuned | 22.73 | { gens = 578, era = 58, retain = 0.40, mutate_prob = 0.33 } |
| 10 | tuned | 22.60 | { gens = 389, era = 184, retain = 0.39, mutate_prob = 0.48 } |
| 11 | tuned | 18.80 | { gens = 429, era = 107, retain = 0.29, mutate_prob = 0.33 } |

### Threats to validity:
- Do we really need an optimizer, optimizing another optimizer? Who will optimize the optimizer, optimizing the optimizer! :) Food for thought.
- This process is time consuming, we might consider to utilize that same time to run our GA on a larger set of candidates, this might give a better result in lesser amount of time.

### Future Work:
- Optimize the algorithm to make it faster. 
- GA Model is currently a single objective function. We might consider modifications to make it a multi-objective model and consider other properties from GA algorithm population such as Energy.
