# IART

> Compile and Run
 Since the project was built in Python, the only requirement for running with the command line is having python3 installed in the OS - it is already built in Linux (or run in IDEs with Python extensions).

 Compiling is not needed with Python, to run the application one must type: python3 main.py <<file_path>>

> How to use
The program is very simple and straight forward:

========================================
=========== Photo Slideshow ============

|         1. Create Slideshow          |
|         2. Quit                      |

|   > Select 1

|------------- Algorithms -------------|
|        1. Hill Climbing              |
|        2. Tabu Search                |
|        3. Simulated Annealing        |
|        4. Genetic Algorithm          |
|        5. Quit                       |

|   > Select  _

2) Each algorithm requires fields that must be specified by the user. The fields and their default values and intervals are defined.
   The option of saving the evolution of the algorithm's processing in a csv file is provided.

For example, in Hill Climbing:
|   > Define maximum number of iterations (over 100 ; 'default' for 1000; -1 for no limit): _
|   > Limit number of initial state slides (None for no limit): _
|   > Do you wish to save the development in csv format (y/n): _

3) Every algorithm during its processing prints the current state in a way the user can understand.

For example, in Hill Climbing:
-------------------------------
Function name :  add_horizontal
Node Score :  34
Number of photos: 150
Number of slides: 101
-------------------------------

4) Prints of different steps are also shown: 

get_initial_state (/home/meias/Work/GitHub/IART/DataStructure/Slideshow.py:208):
    0.007 seconds
// this referres to how much time was spent on developing an initial state

hillClimb (/home/meias/Work/GitHub/IART/SearchTree/Node.py:67):
    0.508 seconds
// this referres to how much time was spent on the algorithm's processing

5) When a solution is determined, the following prints appear, describing the number of slides in the solution, the total score and the output file's name: <algorithm>_solved.txt

--------------- Finished ---------------
Solution: 101 slides
Score: 35
--------- Creating output file ---------
|   Output file: hillclimbing_solved.txt



Note: A few of the inputs don't have validation: for example, when the user inserts a string instead of an integer.