import random
from copy import deepcopy
from collections import deque
import itertools


class NPuzzle:
    
    def __init__(self, N=3, M=None, x=None, y=None):
        self.matrix = []
        self.N = N
        if M is not None:
            self.matrix = M
            self.zero_x = x
            self.zero_y = y
        else:
            sample = random.sample(range(N * N), N * N)
            for i in range(N):
                self.matrix.append([])
            i = 0
            j = 0
            for n in sample:
                self.matrix[j].append(n)
                i += 1
                if i == N:
                    i = 0
                    j = (j + 1) % N
        for i in range(N):
            for j in range(N):
                if self.matrix[i][j] == 0:
                    self.zero_x = i
                    self.zero_y = j
                    return

    def __str__(self):
        st = []
        for n in self.matrix:
            st.append(" ".join(map(str, n)))
        return "\n".join(st)

    def __eq__(self, value):
        return self.matrix.__eq__(value.matrix)

    def __hash__(self):
        has = 0
        for i in self.matrix:
            for j in i:
                has ^= hash(j)
        return has

    @staticmethod
    def up(old):
        Puzzle = deepcopy(old)
        M = Puzzle.matrix
        if old.zero_x > 0:
            M[old.zero_x][old.zero_y] = M[old.zero_x - 1][old.zero_y]
            M[old.zero_x - 1][old.zero_y] = 0
            Puzzle.zero_x -= 1
            return Puzzle
        return None

    @staticmethod
    def down(old):
        Puzzle = deepcopy(old)
        M = Puzzle.matrix
        if old.zero_x < old.N - 1:
            M[old.zero_x][old.zero_y] = M[old.zero_x + 1][old.zero_y]
            M[old.zero_x + 1][old.zero_y] = 0
            Puzzle.zero_x += 1
            return Puzzle
        return None

    @staticmethod
    def left(old):
        Puzzle = deepcopy(old)
        M = Puzzle.matrix
        if old.zero_y > 0:
            M[old.zero_x][old.zero_y] = M[old.zero_x][old.zero_y - 1]
            M[old.zero_x][old.zero_y - 1] = 0
            Puzzle.zero_y -= 1
            return Puzzle
        return None

    @staticmethod
    def right(old):
        Puzzle = deepcopy(old)
        M = Puzzle.matrix
        if old.zero_y < old.N - 1:
            M[old.zero_x][old.zero_y] = M[old.zero_x][old.zero_y + 1]
            M[old.zero_x][old.zero_y + 1] = 0
            Puzzle.zero_y += 1
            return Puzzle
        return None

    @staticmethod
    def solution(N):
        queue = deque([i for i in range(1, N * N)])
        queue.append(0)
        return NPuzzle(N,
                       M=[[queue.popleft() for n in range(N)]
                          for i in range(N)],
                       x=N - 1,
                       y=N - 1)

    @staticmethod
    def gen_puzzle(N, n_moves=10):
        puzzle = NPuzzle.solution(N)
        i = 0
        while i != n_moves:
            funcs = [NPuzzle.up, NPuzzle.down, NPuzzle.right, NPuzzle.left]
            newp = None
            j = random.randint(0, 3)
            while newp is None:
                j = (j + 1) % 4
                newp = funcs[j](puzzle)
            puzzle = newp
            i += 1
        return puzzle

    @staticmethod
    def h1(Puzzle):
        n = 0
        l = list(itertools.chain.from_iterable(Puzzle.matrix))
        l1 = list(
            itertools.chain.from_iterable(NPuzzle.solution(Puzzle.N).matrix))
        for i, j in zip(l, l1):
            if i != j:
                n += 1
        return n

    @staticmethod
    def h2(Puzzle):
        N = Puzzle.N
        i = 0
        j = 0
        n = 0
        l1 = Puzzle.matrix
        solu = NPuzzle.solution(Puzzle.N).matrix
        while i < N:
            while j < N:
                piece = l1[i][j]
                solu_piece = solu[i][j]
                if piece != solu_piece:
                    vec = NPuzzle.correct_position(N, piece)
                    n += abs(i - vec[0]) + abs(j - vec[1])
                j += 1
            i += 1
            j = 0
        return n

    @staticmethod
    def correct_position(N, val):
        if val == 0:
            return [N - 1, N - 1]
        else:
            return [(val - 1) // N, (val - 1) % N]


def __test():
    K = NPuzzle(3)
    print(K)
    print("\n")
    print(K.left())
    print("\n")
    print(K.up())
    print("\n")
    print(K.down())
    print("\n")
    print(K.right())


def __test2():
    n = NPuzzle.gen_puzzle(4, 50)
    print(n)


def __test3():
    n1 = NPuzzle(4)
    n2 = NPuzzle(5)
    print(n1.correct_position(5))
    print(NPuzzle.solution(4))
    print(n2.correct_position(5))
    print(NPuzzle.solution(5))


def __test4():
    N = 5
    n1 = NPuzzle(N)
    for i in range(N * N):
        print(i, n1.correct_position(N, i))


def __test5():
    N = 4
    n1 = NPuzzle.gen_puzzle(N, 10)
    print(n1)
    print(NPuzzle.h1(n1))


def __test6():
    N = 3
    n1 = NPuzzle(N, [[1, 2, 3], [4, 0, 5], [7, 8, 6]])
    n2 = NPuzzle(N, [[1, 2, 3], [4, 5, 0], [7, 8, 6]])
    print(n1, NPuzzle.h2(n1))
    print(n2, NPuzzle.h2(n2))
