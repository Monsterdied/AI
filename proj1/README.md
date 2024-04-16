# Book Scanning

## Introduction

This project is a book scanning project. The goal is to plan which books to scan from which library to maximize the total score of all scanned books, taking into account that each library needs to be signed up before it can ship books.

## Setup

To run the project, go into the project folder. It should look like this: ../IA

Then, run the following command in the terminal:

```bash
py main.py
# or other version of py, you might have. Although, it might require do install some libraries, not sure which ones.
```

## Usage

Before starting, It is necessary to have a folder named "data" with the required data sets.

When running the program, it will ask which option you want to select:

```
Select option:
1 - Main Menu
2 - Test
3 - Exit
```

The first one is to select the main menu, where you can select the data set you want to use and the respective algorithm to solve it.
The second one, although irrelevant for the user, is to run and test the algorithms.

When selecting the first option:

```
Select type of algorithm:
1 - Hill Climbing
2 - Tabu Search
3 - Simmulated Annealing
4 - Genetic Algorithm
5 - Exit
Enter your choice:
```

```
Select file:
0 - a_example.txt
1 - b_read_on.txt
2 - c_incunabula.txt
3 - d_tough_choices.txt
4 - e_so_many_books.txt
5 - f_libraries_of_the_world.txt
Enter your choice: 
```

```
Enter number of iterations: 
```

 - To change the way that the solution is handled is needed to change the imports
    - Using Radom Solution
```python
#from solution import Solution
#BooksSorted = True
from solutionRandom import Solution
BooksSorted = False
```
- Using Greedy Solution
```python
from solution import Solution
BooksSorted = True
#from solutionRandom import Solution
#BooksSorted = False
```

If you wish to do so, you can change the parameters of the algorithms in the respective file, that is, the main.py file.

This project was made by:

| Name | Email |
|-|-|
| Rodrigo Póvoa | up202108890@edu.fe.up.pt |
| Tomnás Sarmento | up202108778@edu.fe.up.pt |
| Tomás Câmara | up202108665@edu.fe.up.pt |
