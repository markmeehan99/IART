from DataStructure.Slide import *
from DataStructure.Photo import *
from Parser.InputParser import *
from SearchTree.Heuristics import *
from SearchTree.InitialState import *

if __name__ == "__main__":
    original_vertical_photos = []
    original_horizontal_photos = []

    parse_input_file(sys.argv[1], original_vertical_photos, original_horizontal_photos)   

    solution = get_solution(original_vertical_photos.copy(), original_horizontal_photos.copy())

    #get N solutions to build a population and then apply genetic algorithms

    print(solution)


def get_solution(vertical_photos, horizontal_photos):
    solution = get_initial_state(vertical_photos, horizontal_photos)

    #apply algorithms

    return solution