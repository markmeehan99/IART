from Node import *
from NPuzzle import *

N = 10

print(NPuzzle.h1(NPuzzle.solution(N)))

for i in range(7):
    t = SearchTree(Node(NPuzzle.gen_puzzle(N,10)))
    n = t.hillClimb([NPuzzle.up, NPuzzle.down, NPuzzle.right, NPuzzle.left], NPuzzle.h2)
    print(n)
# print(n.ancestry())