import collections as q
from profilehooks import timecall
from heapq import heappush
from heapq import heappop
from math import inf
from math import exp
from copy import deepcopy
import random


class Node:
    """ __init__ -> Node constructor
        value  -> <Obj> with at least  __eq__ and __hash__ overloaded
        parent -> <Node> Parent node
        depth  -> <Int> Depth level
        path_cost   -> <Int|Float> Path cost from parent to this node
        func   -> <String> Function name that was applied to generate this node
    """
    def __init__(self, value, parent=None, depth=0, cost=0, func=None):
        self.value = value
        self.parent = parent
        self.children = []
        self.depth = depth
        self.path_cost = 0
        self.func = func

    """ expand -> Generates a new Node that is the result of func applied to self
        func -> <Function> Function that Generates a new Node
        cost -> <Int|Float> Cost of the generation of New Node
    """

    def expand(self, func, cost=0, addchildren=True):
        value = func(self.value)
        if value is None:
            return
        node = Node(value=value,
                    depth=self.depth + 1,
                    cost=cost + self.path_cost,
                    parent=self,
                    func=func.__name__)
        if addchildren:
            self.children.append(node)
        return node

    def __repr__(self):
        return " func={} depth={} value={}".format(str(self.func),
                                                   str(self.depth),
                                                   str(self.value))

    """ ancenstry -> generates an array with the path from the first parent Node with no parent to self
    """

    def ancestry(self):
        ancest = []
        n = self
        while n is not None:
            func_name = "None" if n.func is None else n.func
            ancest.append([n.value, func_name])
            n = n.parent
        return ancest[::-1]

    def __eq__(self, value):
        return self.value.__eq__(value.value)

    def __hash__(self):
        return self.value.__hash__()


class SearchTree:
    def __init__(self, root, startingPlayer=0):
        if isinstance(root, Node):
            self.root = root
        self.queue = q.deque()
        self.heap = []
        self.queue.append(root)
        self.visited = set()

    def resetTree(self):
        self.queue.clear()
        self.heap.clear()
        self.visited.clear()
        self.root.children.clear()

    # Closed Search

    @timecall
    def breadthSearch(self, func, goal=None, checkGoal=None, depth=-1):

        if isinstance(func, list):
            while len(self.queue) != 0:
                n = self.queue.popleft()
                if n in self.visited:
                    continue
                self.visited.add(n)
                for f in func:
                    newnode = n.expand(f)
                    if newnode is None:
                        continue
                    if newnode.depth == depth:
                        continue
                    self.queue.append(newnode)
                    if checkGoal is None:
                        if newnode.value == goal:
                            return newnode
                    else:
                        if checkGoal(newnode):
                            return newnode

    @timecall
    def uniform_cost(self,
                     func,
                     heuristic,
                     goal=None,
                     checkGoal=None,
                     depth=-1):

        order = 0
        if len(self.root.children) == 0:
            heappush(self.heap, (self.root.path_cost, order, self.root))
            order += 1
        if isinstance(func, list):
            while len(self.heap) != 0:
                n = heappop(self.heap)[2]
                if n in self.visited:
                    continue
                self.visited.add(n)
                for f in func:
                    newnode = n.expand(f)
                    if newnode is None:
                        continue
                    if newnode.depth == depth:
                        continue
                    heappush(self.heap, (newnode.path_cost, order, newnode))
                    order += 1
                    if checkGoal is None:
                        if newnode.value == goal:
                            return newnode
                    else:
                        if checkGoal(newnode):
                            return newnode

    @timecall
    def greedySearch(self,
                     func,
                     heuristic,
                     goal=None,
                     checkGoal=None,
                     depth=-1):

        order = 0
        if len(self.root.children) == 0:
            heappush(self.heap, (heuristic(self.root.value), order, self.root))
            order += 1
        if isinstance(func, list):
            while len(self.heap) != 0:
                n = heappop(self.heap)[2]
                if n in self.visited:
                    continue
                self.visited.add(n)
                for f in func:
                    newnode = n.expand(f)
                    if newnode is None:
                        continue
                    if newnode.depth == depth:
                        continue
                    heappush(self.heap,
                             (heuristic(newnode.value), order, newnode))
                    order += 1
                    if checkGoal is None:
                        if newnode.value == goal:
                            return newnode
                    else:
                        if checkGoal(newnode):
                            return newnode

    @timecall
    def a_star(self, func, heuristic, goal=None, checkGoal=None, depth=-1):
        order = 0
        if len(self.root.children) == 0:
            heappush(self.heap,
                     (heuristic(self.root.value) + self.root.path_cost, order,
                      self.root))
            order += 1
        if isinstance(func, list):
            while len(self.heap) != 0:
                n = heappop(self.heap)[2]
                if n in self.visited:
                    continue
                self.visited.add(n)
                for f in func:
                    newnode = n.expand(f)
                    if newnode is None:
                        continue
                    if newnode.depth == depth:
                        continue
                    heappush(self.heap,
                             (heuristic(newnode.value) + newnode.path_cost,
                              order, newnode))
                    order += 1
                    if checkGoal is None:
                        if newnode.value == goal:
                            return newnode
                    else:
                        if checkGoal(newnode):
                            return newnode

    @timecall
    def hillClimb(self, func, heuristic):
        if isinstance(func, list):
            node = self.root
            nodeEval = heuristic(node.value)
            while True:
                nextnode = None
                nextnodeEval = -inf
                for f in func:
                    newnode = node.expand(f)
                    if newnode is not None:
                        newnodeEval = heuristic(newnode.value)
                        if newnodeEval > nextnodeEval:
                            nextnode = newnode
                            nextnodeEval = newnodeEval
                if nodeEval >= nextnodeEval:
                    return node
                node = nextnode
                nodeEval = nextnodeEval

    @timecall
    def tabuSearch(self,
                   func,
                   heuristic,
                   tabuTernure,
                   aspirationCriteria=False,
                   frequency=False,
                   freq_K=0,
                   n_iter=3000):
        if isinstance(func, list) and isinstance(tabuTernure, list):
            if len(func) != len(tabuTernure):
                print("Tabu ternure must be of same length as function lists")
                return
            tabu = [0 for _ in func]
            freq = [0 for _ in func]
            node = self.root
            nodeEval = heuristic(node.value)
            max_iter = n_iter
            while max_iter != 0:
                nextnode = None
                nextnodeEval = -inf
                nextnodeIndex = -1
                asps = []
                for i, f in enumerate(func):
                    if tabu[i] != 0:
                        if aspirationCriteria:
                            asps.append(f)
                        tabu[i] -= 1
                        continue
                    newnode = node.expand(f, False)
                    if newnode is None:
                        continue
                    tabu[i] = tabuTernure[i]
                    if frequency:
                        newnodeEval = heuristic(
                            newnode.value) - freq_K * freq[i]
                    else:
                        newnodeEval = heuristic(newnode.value)
                    if newnodeEval > nextnodeEval:
                        nextnode = newnode
                        nextnodeEval = newnodeEval
                        if frequency:
                            nextnodeIndex = i
                if nextnode is None:
                    if aspirationCriteria:
                        for i, f in enumerate(asps):
                            newnode = node.expand(f, False)
                            if newnode is None:
                                continue
                            tabu[i] = tabuTernure[i]
                            if frequency:
                                newnodeEval = heuristic(
                                    newnode.value) - freq_K * freq[i]
                            else:
                                newnodeEval = heuristic(newnode.value)
                            if newnodeEval > nextnodeEval:
                                nextnode = newnode
                                nextnodeEval = newnodeEval
                                if frequency:
                                    nextnodeIndex = i
                    if nextnode is None:
                        return node
                if nodeEval >= nextnodeEval:
                    max_iter -= 1
                    node = nextnode
                    nodeEval = nextnodeEval
                    if frequency:
                        freq[nextnodeIndex] += 1

    @timecall
    def simulated_annealing(self, func, heuristic, init_T, alpha):
        if len(func) == 0:
            return
        node = self.root
        nodeEval = heuristic(self.root.value)
        T = init_T
        delta_e = nodeEval
        while round(T) != 0:
            nextnode = func[random.randint(0, len(func) - 1)](node.value)
            nextEval = heuristic(nextnode.value)
            delta_e = nextEval - nodeEval
            if delta_e > 0:
                node = nextnode
            else:
                if random.random() <= (1 / (1 + exp(-delta_e / T))):
                    node = nextnode
            T = alpha(T)
        return node

