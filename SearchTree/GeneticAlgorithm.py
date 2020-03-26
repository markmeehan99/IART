from DataStructure.Slideshow import *
import random
from copy import deepcopy
from profilehooks import timecall


def geneticAlgorithm(initial_population, fitness):
    scores = list(map(fitness, population))
    population = selection(initial_population, scores)

def choice(objects, weights):
    total_weight = sum(weights)
    chances = [i / total_weight for i in weights]
    x = random.random()
    for i in range(len(chances)):
        if i != 0:
            chances[i] += chances[i - 1]
        if x < chances[i]:
            return deepcopy(objects[i])

@timecall
def selection(population, fitnesses, N):
    if N is None:
      N = len(population)
    return [choice(population, fitnesses) for x in range(N)]
