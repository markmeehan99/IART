from DataStructure.Slideshow import *
import random
from copy import deepcopy
from profilehooks import timecall


def geneticAlgorithm(initial_population, fitness, no_generations):
    population = initial_population

    for n in range(no_generations):
        # Reproduction
        population = reproduction(population)

        # Mutation

        # Selection
        scores = list(map(fitness, population))
        population = selection(population, fitness)
        printGeneration(population, scores, n)

    return max(population)


def choice(objects, weights):
    total_weight = sum(weights)
    chances = [i / total_weight for i in weights]
    x = random.random()
    for i in range(len(chances)):
        if i != 0:
            chances[i] += chances[i - 1]
        if x > chances[i]:
            return deepcopy(objects[i])


def choiceByCombat(population, fitness, N=None):
    pop_size = len(population) if N is None else N

    [f1, f2] = [random.choice(population), random.choice(population)]

    return deepcopy(f1 if fitness(f1) >= fitness(f2) else f2)


@timecall
def selection(population, fitness, N=None):
    if N is None:
        N = len(population)
    return [choiceByCombat(population, fitness) for x in range(N)]


@timecall
def reproduction(population, elitism=True):
    if elitism:
        pairs = generateElitPairsExtreme(population)
    else:
        pairs = generateRandomPairs(len(population))
    result = []
    for i in pairs:
        p1 = population[i[0]]
        p2 = population[i[1]]
        sons = p1.reproduce(p1, p2)
        son = max(sons)
        result.append(son)
    return result


def generateRandomPairs(population):
    k = len(population)
    ids = set([x for x in range(k)])
    result = []
    while k != 0:
        pair = random.sample(ids, 2)
        result.append(pair)
        k -= 1
    return result


def generateElitPairs(population):
    p = sorted(population)
    k = len(population)
    result = []
    while k != 0:
        best_parent = random.randint(k // 2, k - 1)
        worst_parent = random.randint(0, k - 1)
        result.append([best_parent, worst_parent])
        k -= 1
    return result


def generateElitPairsExtreme(population):
    p = sorted(population)
    k = len(population)
    result = []
    bests_parents = p[k // 2:k - 1]
    b_size = len(bests_parents)
    i = 0
    while k != 0:
        best_parent = i
        worst_parent = random.randint(0, k - 1)
        result.append([best_parent, worst_parent])
        i = (i + 1) % b_size
        k -= 1
    return result


def printGeneration(pop, scores, n):
    print("Generation " + str(n) + ":")
    print("Scores: " + str(sorted(scores)))
    print("Min : " + str(min(scores)))
    print("Max : " + str(max(scores)))
    print("Avg : " + str(sum(scores) / len(scores)))
