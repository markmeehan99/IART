from DataStructure.Slideshow import *
import random
from copy import deepcopy
from profilehooks import timecall


def geneticAlgorithm(initial_population, fitness, no_generations):
    population = initial_population

    for n in range(N):
        # Reproduction
        population = reproduction(population)

        # Mutation

        # Selection
        scores = list(map(fitness, population))
        population = selection(initial_population, scores)

    return max(population)


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


@timecall
def reproduction(population):
    pairs = generateRandomPairs(len(population))
    result = []
    for i in pairs:
        p1 = population[i[0]]
        p2 = population[i[1]]
        result.append(p1.reproduce(p1, p2))
    return result


def generateRandomPairs(size):
    ids = set([x for x in range(size)])
    result = []
    while len(ids) != 0:
        pair = random.sample(ids, 2)
        for i in pair:
            ids.remove(i)
        result.append(pair)
    return result


def printGeneration(pop, scores, n):
    print("Generation 1 :")
    print("")
