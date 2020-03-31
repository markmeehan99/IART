import collections as q
from profilehooks import timecall
from heapq import heappush
from heapq import heappop
from math import inf
from math import exp
from copy import deepcopy
import random


@timecall
def simulated_annealing(init, func, heuristic, init_T, alpha, to_csv):
    step = 0
    if len(func) == 0:
        return
    node = init
    nodeEval = heuristic(init)
    bestNode = node
    bestEval = nodeEval
    T = init_T
    delta_e = nodeEval

    if to_csv:
        file = open("simulated_annealing.csv", "w")

    while round(T) != 0:
        nextnode = None
        while nextnode is None:
            nextnode = func[random.randint(0, len(func) - 1)](node)
        nextEval = heuristic(nextnode)
        delta_e = nextEval - nodeEval
        if delta_e > 0:
            node = nextnode
            nodeEval = nextEval
        else:
            if random.random() <= (1 / (1 + exp(-delta_e / T))):
                node = nextnode
                nodeEval = nextEval
        if nodeEval >= bestEval:
            bestNode = node
            bestEval = nodeEval
        T += -alpha * T
        print(step, ",", nextEval, ",", T)
        
        if to_csv:
            s = str(step) + "," +  str(nextEval) + "\n"
            file.write(s)

        step += 1
    return bestNode


@timecall
def hillClimb(init_sol, func, heuristic, to_csv=False, iter_max=-1):
    if isinstance(func, list):
        iteration = 0
        file = None
        if to_csv:
            file = open("hillClimb.csv", "w")
        node = init_sol
        nodeEval = heuristic(init_sol)
        while True:
            nextnode = None
            nextnodeEval = -inf
            nextnodefunc = None
            for f in func:
                newnode = f(node)
                if newnode is not None:
                    newnodeEval = heuristic(newnode)
                    if newnodeEval > nextnodeEval:
                        nextnode = newnode
                        nextnodeEval = newnodeEval
                        nextnodefunc = f.__name__
            if nodeEval >= nextnodeEval or iter_max == iteration:
                if to_csv:
                    file.close() if file is not None else file
                return node
            node = nextnode
            nodeEval = nextnodeEval
            print("-------------------------------")
            print("Function name : ", nextnodefunc)
            print("Node Score : ", nodeEval)
            pl = getattr(node, "plusInfo", None)
            if callable(pl):
                print(node.plusInfo())
            print("-------------------------------")
            if to_csv:
                s = str(iteration) + "," +  str(nodeEval) + "\n"
                file.write(s)
            iteration += 1
        if to_csv:
            file.close() if file is not None else file
        return node


@timecall
def tabuSearch(init_sol,
               funcs,
               heuristic,
               iter_between_improvements=200,
               to_csv=False,
               iter_max=-1):
    tabu = [0 for _ in range(len(funcs))]
    tabuTernure = len(funcs) - 2
    nextnode = init_sol
    nextnodeEval = heuristic(nextnode)
    bestNode = nextnode
    bestNodeEval = nextnodeEval
    file = None
    iteration = 0
    if to_csv:
        file = open("tabuSearch.csv", "w")
    iter_bet = 0
    while iter_bet <= iter_between_improvements and iter_max != iteration:
        # Find max allowed Neighbour
        maxNeighbour = None
        maxNeighbourEval = -inf
        indexToTabu = -1
        for i, f in enumerate(funcs):
            if tabu[i] > 0:
                tabu[i] -= 1
                continue
            neighbour = f(nextnode)
            if neighbour is None:
                continue
            neighbourEval = heuristic(neighbour)
            if maxNeighbour is None or neighbourEval > maxNeighbourEval:
                maxNeighbour = neighbour
                maxNeighbourEval = neighbourEval
                indexToTabu = i
        # Forbid neighbour for n iterations
        tabu[indexToTabu] = tabuTernure
        nextnode = maxNeighbour
        nextnodeEval = maxNeighbourEval
        # Update best node
        iter_bet += 1
        if nextnodeEval > bestNodeEval:
            bestNode = nextnode
            bestNodeEval = nextnodeEval
            iter_bet = 0
        if to_csv:
            s = str(iteration) + "," + str(bestNodeEval) + "\n"
            file.write(s)
        print("-------------------------------")
        print("Iter since best solution update: ", iter_bet)
        print("Best score : ", bestNodeEval)
        pl = getattr(bestNode, "plusInfo", None)
        if callable(pl):
            print(bestNode.plusInfo())
        print("Node Score : ", nextnodeEval)
        print("Function name : ", funcs[indexToTabu].__name__)
        print("-------------------------------")
        iteration += 1
    if to_csv:
        file.close() if file is not None else file
    return bestNode
