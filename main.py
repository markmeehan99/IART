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
def gen_N(N):
    s = []
    for i in range(N):
        s.append(Slideshow.get_initial_state(300, True))
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



def display_create_slideshow():
    while(True):
        file_path = input("|   Insert file's path ('q' to quit): ")

        if file_path == 'q':
            break
        elif path.exists(file_path):
            parse_input_file(file_path)
            display_algorithm_options()
        else: print("|-------- File does not exist ---------|")

def display_algorithm_options():
    while(True):
        print("")
        print("|------------- Algorithms -------------|")
        print("|        1. Hill Climbing              |")
        print("|        2. Tabu Search                |")
        print("|        3. Simulated Annealing        |")
        print("|        4. Genetic Algorithm          |")
        print("|        5. Quit                       |")
        print("")
        
        option = input("|   Select  ")

        if option == "1":
            hill_climbing_option()
        elif option == "2":
            tabu_search_option()
        elif option == "3":
            simulated_annealing_option()
        elif option == "4":
            genetic_algorithm_option()
        else: print("-------- Select a valid option! --------")

def initial_state_size():
    while True:
        size = input("|   Limit number of initial state slides (None for no limit): ")
        if size == "None":
            size = None
        else:
            size = int(size)
            if size <= 0:
                print("------------ Invalid value -------------")
                continue
        return size

def get_csv_option():
    while True:
        csv = input("|   Do you wish to save the development in csv format (y/n): ")

        if csv == "y":
            csv = True
        elif csv == "n":
            csv = False
        else:
            print("------------ Invalid value -------------")
            continue
        return csv

def hill_climbing_option():
    while True:
        iter_max = input("|   Define maximum number of iterations (over 100 ; 'default' for 1000): ")
        if iter_max == "default":
            iter_max = 1000
        else:
            iter_max = int(iter_max)
            if iter_max < 100:
                print("------------ Invalid value -------------")
                continue
        break

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)

    operators = [
        Slideshow.add_horizontal,
        Slideshow.add_vertical,
        Slideshow.add_horizontal,
        Slideshow.add_vertical,
        Slideshow.remove_smallest_transition,
        Slideshow.remove_random_slide,
        Slideshow.remove_random_slide,
        Slideshow.trade_random,
        Slideshow.trade_random,
        Slideshow.trade_random,
        Slideshow.shuffle
    ]

    hillClimb(slideshow, operators, Slideshow.getScore, csv, iter_max)

    print("--------------- Finished ---------------")
    print("Solution: " + str(slideshow))
    print("Score: " + str(slideshow.getScore))
    

def tabu_search_option():
    while True:
        n_interations = input("|   Define stop criteria: number of iterations after the best score found (over 25 ; 'default' for 100): ")
        if n_interations == "default":
            n_interations = 100
        else:
            n_interations = int(n_interations)
            if n_interations < 25:
                print("------------ Invalid value -------------")
                continue
        break
    while True:
        iter_max = input("|   Define maximum number of iterations (over 100 ; 'default' for 1000): ")
        if iter_max == "default":
            iter_max = 1000
        else:
            iter_max = int(iter_max)
            if iter_max < 100:
                print("------------ Invalid value -------------")
                continue
        break

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)

    operators = [
        Slideshow.add_horizontal,
        Slideshow.add_vertical,
        Slideshow.add_horizontal,
        Slideshow.add_vertical,
        Slideshow.remove_smallest_transition,
        Slideshow.remove_random_slide,
        Slideshow.remove_random_slide,
        Slideshow.trade_random,
        Slideshow.trade_random,
        Slideshow.trade_random,
        Slideshow.shuffle
    ]
    
    tabuSearch(slideshow, operators, Slideshow.getScore, csv, n_interations, iter_max)

    print("--------------- Finished ---------------")
    print("Solution: " + str(slideshow))
    print("Score: " + str(slideshow.getScore))


def simulated_annealing_option():
    while True:
        init_T = input("|   Insert initial temperature (over 1000 | 'default' for default=1000000): ")
        if init_T == "default":
            init_T = 10**5
        else:
            init_T = int(init_T)
            if init_T < 1000:
                print("------------ Invalid value -------------")
                continue
        break
        
    while True:
        alpha = input("|   Insert alpha (in ]0,1[ ; 'default' for 0.01): ")
        if alpha == "default":
            alpha = 0.01
        else:
            alpha = float(alpha)
            if alpha <= 0 and alpha >= 1:
                print("------------ Invalid value -------------")
                continue
        break

    size = initial_state_size()

    csv = get_csv_option()

    exactly = True if size != None else False
    slideshow = Slideshow.get_initial_state(size, exactly)
    
    operators = [
        Slideshow.add_horizontal, 
        Slideshow.add_vertical, 
        Slideshow.remove_smallest_transition, 
        Slideshow.trade_random, 
        Slideshow.trade_random
    ]

    simulated_annealing(slideshow, operators, Slideshow.getScore, init_T, alpha, csv)

    print("--------------- Finished ---------------")
    print("Solution: " + str(slideshow))
    print("Score: " + str(slideshow.getScore))


def genetic_algorithm_option(): 
    while True:
        n_population = input("|   Insert number of initial population (in ]0,100] ; 'default' for 30): ")
        if n_population == "default":
            n_population = 30
        else:
            n_population = int(n_population)
            if n_population <= 0 and n_population > 100:
                print("------------ Invalid value -------------")
                continue
        break

    while True:
        n_generations = input("|   Insert number of generations (in ]0,100] ; 'default' for 30): ")
        if n_generations == "default":
            n_generations = 30
        else:
            n_generations = int(n_generations)
            if n_generations <= 0 and n_generations > 100:
                print("------------ Invalid value -------------")
                continue
        break

    csv = get_csv_option()

    population = gen_N(n_population)

    slideshow = geneticAlgorithm(population, Slideshow.getScore, n_generations, csv)

    print("--------------- Finished ---------------")
    print("Solution: " + str(slideshow))
    print("Score: " + str(slideshow.getScore))


if __name__ == "__main__":
    print("========================================")
    print("=========== Photo Slideshow ============")

    while(True):
        print("")
        print("|         1. Create Slideshow          |")
        print("|         2. Quit                      |")
        print("")

        option = input("|   Select ")

        if option == "1":
            display_create_slideshow()
        elif option == "2":
            print("")
            print("=============== Goodbye ================")
            print("")
            exit(0)
        else: print("-------- Select a valid option! --------")
