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


def test_splice(s1=None, s2=None):
    if s1 == None:
        s1 = Slideshow.get_initial_state(300, True)
    if s2 == None:
        s2 = Slideshow.get_initial_state(300, True)
    print(s1.calcFullScore())
    print(s2.calcFullScore())
    print("children:")
    [s3, s4] = Slideshow.reproduce(s1, s2)
    print(s3.calcFullScore())
    print(s4.calcFullScore())
    print(" ")


if __name__ == "__main__":
    original_vertical_photos = []
    original_horizontal_photos = []

    parse_input_file(sys.argv[1])
    s1 = Slideshow.get_initial_state(30, True)
    s2 = Slideshow.get_initial_state(31, True)
    for i in range(10):
        print("Splice " + str(i) + ":")
        test_splice()
