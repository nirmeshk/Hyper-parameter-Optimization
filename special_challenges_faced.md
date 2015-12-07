# Special Challenges faced

- Code 8 was smooth.
- Code 9 challenges:
    + Figuring out correct GA algorithm. There are so many variations of GA floating around, it was dificult to figure out what works for this project
    + Using visual aids to see if algorithm i actually optimizing the population.
    + Bdom vs Cdom challenge.
    + Lack of variation (spread) in population because of Elite sampling.
- Code 10 challenges:
    + Slow performance of GA.
    + Used some form of memmoization to speedup things little bit. And it helped!!
    + Difficulat to debug even small mistakes: seed of random, keeping same baseline population for all ga optimized by DE.
    + A good objective score to measure for 1) Early termination 2) Comparing different GA optimizers.
    + Even tried some easy models, but those models lack interesing results as they are easily optimized in very few generations. Also, the GA code n*n was the main culprit after we did some profiling.
