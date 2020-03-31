from DataStructure import *
from DataStructure.Photo import *
from Parser.InputParser import *
from profilehooks import timecall
from SearchTree.GeneticAlgorithm import geneticAlgorithm
from SearchTree.GeneticAlgorithm import generateRandomPairs
from SearchTree.Node import *

import os.path
from os import path


@timecall
def gen_N(N,size=2000):
    s = []
    for i in range(N):
        s.append(Slideshow.get_initial_state(size,True))
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


def display_algorithm_options():
    while (True):
        print("")
        print("|------------- Algorithms -------------|")
        print("|        1. Hill Climbing              |")
        print("|        2. Tabu Search                |")
        print("|        3. Simulated Annealing        |")
        print("|        4. Genetic Algorithm          |")
        print("|        5. Quit                       |")
        print("")

        option = input("|   > Select  ")

        if option == "1":
            hill_climbing_option()
        elif option == "2":
            tabu_search_option()
        elif option == "3":
            simulated_annealing_option()
        elif option == "4":
            genetic_algorithm_option()
        elif option == "5":
            return
        else:
            print("-------- Select a valid option! --------")


def get_iter_max():
    while True:
        iter_max = input("|   > Define maximum number of iterations (over 100 ; 'default' for 1000; -1 for no limit): ")
        if iter_max == "default" or iter_max == '':
            iter_max = 1000
        else:
            iter_max = int(iter_max)
            if iter_max < 100 and iter_max != -1:
                print("------------ Invalid value -------------")
                continue
        return iter_max

def initial_state_size():
    while True:
        size = input("|   > Limit number of initial state slides (None for no limit): ")
        if size == "None" or size == '':
            size = None
        else:
            size = int(size)
            if size <= 0:
                print("------------ Invalid value -------------")
                continue
        return size


def get_csv_option():
    while True:
        csv = input(
            "|   > Do you wish to save the development in csv format (y/n): ")

        if csv == "y":
            csv = True
        elif csv == "n":
            csv = False
        else:
            print("------------ Invalid value -------------")
            continue
        return csv

def finish(slideshow, algorithm):
    print("--------------- Finished ---------------")
    print("Solution: " + str(len(slideshow.slides)) + " slides")
    print("Score: " + str(Slideshow.getScore(slideshow)))
    print("--------- Creating output file ---------")
    file_name = algorithm + "_solved.txt"

    solution = open(file_name, "w")

    solution.write("File: " + sys.argv[1] + "\n")
    solution.write("Score: " + str(len(slideshow.slides)) + "\n")
    solution.write(str(slideshow) + "\n")
    solution.close()

    print("|   Output file: " + file_name)


def hill_climbing_option():
    iter_max = get_iter_max()

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)

    operators = [
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.remove_smallest_transition, Slideshow.remove_random_slide,
        Slideshow.remove_random_slide, Slideshow.trade_random,
        Slideshow.trade_random, Slideshow.trade_random, Slideshow.shuffle
    ]

    slideshow = hillClimb(slideshow, operators, Slideshow.getScore, csv, iter_max)

    finish(slideshow, "hillclimbing")
    

def tabu_search_option():
    iter_max = get_iter_max()

    while True:
        n_iterations = input("|   > Define stop criteria: number of iterations after the best score found (over 25 ; 'default' for 100): ")
        if n_iterations == "default" or n_iterations == '':
            n_iterations = 100
        else:
            n_iterations = int(n_iterations)
            if n_iterations < 25:
                print("------------ Invalid value -------------")
                continue
        break

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)

    operators = [
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.remove_smallest_transition, Slideshow.remove_random_slide,
        Slideshow.remove_random_slide, Slideshow.trade_random,
        Slideshow.trade_random, Slideshow.trade_random, Slideshow.shuffle
    ]

    slideshow = tabuSearch(slideshow, operators, Slideshow.getScore, n_iterations, csv, iter_max)

    finish(slideshow, "tabusearch")


def simulated_annealing_option():
    while True:
        init_T = input("|   > Insert initial temperature (over 1000 | 'default' for default=1000000): ")
        if init_T == "default" or init_T == '':
            init_T = 10**5
        else:
            init_T = int(init_T)
            if init_T < 1000:
                print("------------ Invalid value -------------")
                continue
        break

    while True:
        alpha = input("|   > Insert alpha (in ]0,1[ ; 'default' for 0.01): ")
        if alpha == "default" or alpha == '':
            alpha = 0.01
        else:
            alpha = float(alpha)
            if alpha <= 0 or alpha >= 1:
                print("------------ Invalid value -------------")
                continue
        break

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)

    operators = [
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.remove_smallest_transition, Slideshow.trade_random,
        Slideshow.trade_random
    ]

    slideshow = simulated_annealing(slideshow, operators, Slideshow.getScore, init_T, alpha, csv)

    finish(slideshow, "simulatedannealing")


def genetic_algorithm_option():
    while True:
        n_population = input("|   > Insert number of initial population (in ]0,100] ; 'default' for 30): ")
        if n_population == "default" or n_population == '':
            n_population = 30
        else:
            n_population = int(n_population)
            if n_population <= 0 or n_population > 100:
                print("------------ Invalid value -------------")
                continue
        break

    while True:
        individual_size = input("|   > Insert size of initial solution of each individual (over 0 ; 'default' for 100): ")
        if individual_size == "default" or individual_size == '':
            individual_size = 100
        else:
            individual_size = int(individual_size)
            if individual_size <= 0:
                print("------------ Invalid value -------------")
                continue
        break

    while True:
        n_generations = input("|   > Insert number of generations (in ]0,100] ; 'default' for 30): ")
        if n_generations == "default" or n_generations == '':
            n_generations = 30
        else:
            n_generations = int(n_generations)
            if n_generations <= 0 or n_generations > 100:
                print("------------ Invalid value -------------")
                continue
        break

    while True:
        mutation = input("|   > Do you wish to mutate (y/n): ")
        if mutation == "y":
            mutation = True

            while True:
                mutation_chance = input("|   > Insert mutation chance (in ]0,1[ ; 'default' for 0.05): ")
                if mutation_chance == "default" or mutation_chance == '':
                    mutation_chance = 0.05
                else:
                    mutation_chance = float(mutation_chance)
                    if mutation_chance <= 0 or mutation_chance >= 1:
                        print("------------ Invalid value -------------")
                        continue
                break

        elif mutation == "n":
            mutation = False
        else:
            print("------------ Invalid value -------------")
            continue
        break

    csv = get_csv_option()

    population = gen_N(n_population)

    operators = [
        Slideshow.add_horizontal, Slideshow.add_vertical,
        Slideshow.remove_smallest_transition, Slideshow.trade_random,
        Slideshow.trade_random
    ]

    slideshow = geneticAlgorithm(population, Slideshow.getScore, n_generations,mutations=operators,to_csv=csv)

    finish(slideshow, "geneticalgorithm")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error in call. Usage: python3 main <file_path>")
        exit(-1)

    parse_input_file(sys.argv[1])

    print("========================================")
    print("=========== Photo Slideshow ============")

    while (True):
        print("")
        print("|         1. Create Slideshow          |")
        print("|         2. Quit                      |")
        print("")

        option = input("|   > Select ")

        if option == "1":
            display_algorithm_options()
        elif option == "2":
            print("")
            print("=============== Goodbye ================")
            print("")
            exit(0)
        else:
            print("-------- Select a valid option! --------")
