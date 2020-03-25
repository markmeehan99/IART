from DataStructure import *
from DataStructure.Photo import *
from Parser.InputParser import *
from profilehooks import timecall


@timecall
def gen_N(N):
    s = []
    for i in range(N):
        s.append(Slideshow.get_initial_state())
        print(i,len(s[-1]))
    return s



if __name__ == "__main__":
    original_vertical_photos = []
    original_horizontal_photos = []

    parse_input_file(sys.argv[1])

    # print(Slideshow.vertical_photos_pool)
    # print(Slideshow.horizontal_photos_pool)
    # s = []
    # for x in range(10):
    #     s.append(Slideshow.get_initial_state())
    s = gen_N(1)

