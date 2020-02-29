import collections as q


class Node:
    """ __init__ -> Node constructor
        value  -> <Obj> with at least  __eq__  overloaded
        parent -> <Node> Parent node
        depth  -> <Int> Depth level
        cost   -> <Int> Path cost from parent to this node
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
    def expand(self, func, cost=0):
        value = func(self.value)
        if value is None:
            return
        node = Node(value=value,
                    depth=self.depth + 1,
                    cost=cost,
                    parent=self,
                    func=func.__name__)
        self.children.append(node)
        return node

    def __repr__(self):
        return " func={} depth={} value={}".format(str(self.func),str(self.depth), str(self.value))

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


class NodeTree:
    def __init__(self, root):
        if isinstance(root, Node):
            self.root = root
        self.queue = q.deque()
        self.queue.append(root)

    def breadthSearch(self, func, goal=None, checkGoal=None, depth=-1):
        if isinstance(func, list):
            while len(self.queue) != 0:
                n = self.queue.popleft()
                for f in func:
                    newnode = n.expand(f)
                    if newnode is None:
                        continue
                    if newnode.depth == depth:
                        return None
                    self.queue.append(newnode)
                    if checkGoal is None:
                        if newnode.value == goal:
                            return newnode
                    else:
                        if checkGoal(newnode):
                            return newnode


# def add(value):
#     return value + "a"

# def add1(value):
#     return value + "b"

# T = NodeTree(Node("a"))
# node = T.breadthSearch([add, add1], goal="ababa")
# print(node.ancestry())

# exit(0)
