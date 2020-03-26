from DataStructure import *
from DataStructure.Photo import *
from Parser.InputParser import *
from profilehooks import timecall


@timecall
def gen_N(N):
    s = []
    for i in range(N):
        s.append(Slideshow.get_initial_state(100))
    return s



if __name__ == "__main__":
    original_vertical_photos = []
    original_horizontal_photos = []

    parse_input_file(sys.argv[1])

    s1 = Slideshow.get_initial_state(4,True)
    s2 = Slideshow.get_initial_state(4, True)
    print(s1)
    print(s2)
    print("children:")
    for i in Slideshow.reproduce(s1, s2):
        print(i)
    
