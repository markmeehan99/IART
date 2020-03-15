from Slide import *
from Photo import *
from heuristics import *

if __name__ == "__main__":
    p1 = Photo(1, "H", ["garden", "cat"])
    p2 = Photo(2, "V", ["smile", "garden"])
    p3 = Photo(3, "V", ["selfie", "garden"])

    s1 = Slide([p1])
    s2 = Slide([p2, p3])

    print(getScore(s1.tags, s2.tags))

# print(vars())