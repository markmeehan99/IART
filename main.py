from Slide import *
from Photo import *
if __name__ == "__main__":
    p1 = Photo(1, "V", ["selfie", "outdoors"])
    p2 = Photo(2, "V", ["selfie", "house"])
    s1 = Slide([p1,p2])

print(vars(s1))