from DataStructure.Slideshow import *
import random
from copy import deepcopy
from profilehooks import timecall


def geneticAlgorithm(initial_population,
                     fitness,
                     no_generations,
                     mutations=None,
                     mutate_chance=0.05,
                     to_csv=False):
    population = initial_population
    file = None
    best = None
    if to_csv:
        file = open("Genetic_algorithm.csv", "w")
        file.write("Generation,Min,Max,Average\n")

    print(list(map(fitness, population)))
    for n in range(no_generations):
        # Reproduction
        population = reproduction(population)

        # Mutation
        if mutations is not None:
            if isinstance(mutations, list):
                n_genes = 0
                for j in range(len(population)):
                    x = random.random()
                    if x <= mutate_chance:
                        n_genes += 1
                        mutation = random.choice(mutations)
                        population[j] = mutation(population[j])
                print(str(n_genes) + " mutations")
        # Selection
        population = selection(population, fitness)
        #elitism
        pbest = max(population) 
        best = pbest if best == None or pbest > best else best 
        scores = list(map(fitness, population))
        printGeneration(population, scores, n, file)
    if file is not None:
        file.close()
    return best


def choice(objects, weights):
    total_weight = sum(weights)
    chances = [i / total_weight for i in weights]
    x = random.random()
    for i in range(len(chances)):
        if i != 0:
            chances[i] += chances[i - 1]
        if x < chances[i]:
            return deepcopy(objects[i])


def choiceByCombat(population, fitness, N=None):
    [f1, f2] = [random.choice(population), random.choice(population)]

    return deepcopy(f1 if fitness(f1) >= fitness(f2) else f2)


@timecall
def selection(population, fitness, N=None, bycombat=None):
    if N is None:
        N = len(population)
    result = []
    bycombat = random.choice([True, False]) if bycombat is  None else bycombat
    if bycombat:
        print("Choice by Combat")
        result = [choiceByCombat(population, fitness) for x in range(N)]
    else:
        print("Choice by weight")
        fitnesses = list(map(fitness, population))
        result = [choice(population, fitnesses) for x in range(N)]
    return result


@timecall
def reproduction(population, elitism=False):
    if elitism:
        pairs = generateElitPairsExtreme(population)
    else:
        pairs = generateRandomPairs(population)
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


def printGeneration(pop, scores, n, file):
    minp = min(scores)
    maxp = max(scores)
    avg = round(sum(scores) / len(scores))
    print("Generation " + str(n) + ":")
    print("Scores: " + str(sorted(scores)))
    print("Min : " + str(minp))
    print("Max : " + str(maxp))
    print("Avg : " + str(avg))
    if file is not None:
        s = str(n) + "," + str(minp) + "," + str(maxp) + "," + str(avg) + "\n"
        file.write(s)
