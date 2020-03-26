from DataStructure import *
from DataStructure.Photo import *
from Parser.InputParser import *
from profilehooks import timecall
from SearchTree.GeneticAlgorithm import geneticAlgorithm


@timecall
def gen_N(N):
    s = []
    for i in range(N):
        s.append(Slideshow.get_initial_state(2500,True))
        print(i)
    return s


def test_splice(s1=None, s2=None):
    if s1 == None:
        s1 = Slideshow.get_initial_state()
    if s2 == None:
        s2 = Slideshow.get_initial_state()
    print(s1.calcFullScore(), len(s1.current_photo_ids))
    print(s2.calcFullScore(), len(s2.current_photo_ids))
    print("children:")
    [s3, s4] = Slideshow.reproduce(s1, s2)
    print(s3.calcFullScore())
    print(s4.calcFullScore())
    print(" ")
    return [s3, s4]


@timecall
def test_nsplices(N):
    s1 = Slideshow.get_initial_state()
    s2 = Slideshow.get_initial_state()
    for i in range(N):
        print("Splice " + str(i) + ":")
        [s1, s2] = test_splice(s1, s2)


if __name__ == "__main__":
    original_vertical_photos = []
    original_horizontal_photos = []

    parse_input_file(sys.argv[1])
    pop = gen_N(30)
    newpop = geneticAlgorithm(pop, Slideshow.getScore)
    print(sorted(list(map(Slideshow.getScore, newpop))))
