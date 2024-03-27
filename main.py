
from library import Library
from book import Book
from sortedcontainers import SortedList
from concurrent.futures import ThreadPoolExecutor
import time
import copy
import numpy as np
#from solution import Solution
#BooksSorted = True
from solutionRandom import Solution
BooksSorted = False
class DataManager:    

    # ------------------------------------read data -----------------------------------
    def __init__(self,filename):
        self.filename = "./data/" + filename
        self.libraries = {}
        self.books = []
        self.signTimeToLibraries = {}
        file1 = open(self.filename, 'r')
        line = file1.readline()
        self.read_first_line_info(line)
        line = file1.readline()
        self.read_books_rating(line)
        line = file1.readline()
        libraryId = 0
        while line != "\n":
            line2 = file1.readline() #comment
            self.read_library_data(libraryId,line,line2)
            libraryId += 1
            line = file1.readline()
        if libraryId != self.nLibraries:
            print("Number of libraries read is not equal to the number of libraries mentioned in the file rating")
        file1.close()
            
            

    def read_first_line_info(self,line):
        data = line.split(' ')
        self.nBooks = int(data[0])
        self.nLibraries = int(data[1])
        self.nDays = int(data[2])

    def read_books_rating(self,line):
        data = line.split(' ')
        i = 0
        for rating in data:
            self.books.append(int(rating))
            i += 1
        if i != self.nBooks:
            print("Error in reading book rating\nNumber of books read is not equal to the number of books mentioned in the file rating")

    def read_library_data(self,libraryId,firstLine,secondLine):
        data = firstLine.split(' ')
        nbooks = int(data[0])
        signTime = int(data[1])
        if(signTime in self.signTimeToLibraries.keys()):
            self.signTimeToLibraries[signTime].append(libraryId)
        else:
            self.signTimeToLibraries[signTime] = [libraryId]
        canShipBooksPerDay = int(data[2])
        bookIds = secondLine.split(' ')
        if BooksSorted:
            LibraryBooks = SortedList()
            i = 0
            for bookid in bookIds:# pode se alterar o ordered set para lista la a frente é so necessario ordenar mas para ja vamos tentar assim
                LibraryBooks.add(Book(self.books[int(bookid)],int(bookid)))
                i += 1
            self.libraries[libraryId] = Library(nbooks,signTime,canShipBooksPerDay,LibraryBooks)
            if i != nbooks:
                print("Number of books from library read is not equal to the number of books mentioned in the file rating")
        else:
            LibraryBooks = np.array([],dtype=int)
            i = 0
            for bookid in bookIds:# pode se alterar o ordered set para lista la a frente é so necessario ordenar mas para ja vamos tentar assim
                LibraryBooks = np.append(LibraryBooks,int(bookid))
                i += 1
            self.libraries[libraryId] = Library(nbooks,signTime,canShipBooksPerDay,LibraryBooks)
            if i != nbooks:
                print("Number of books from library read is not equal to the number of books mentioned in the file rating")

    # ------------------------------------Print data-----------------------------------
    def print_libraries(self):
        for library in self.libraries:
            print("Library: " + str(library))
            print("Books: ")
            for book in self.libraries[library].books:
                print("id:" + str(book.book_id) + " rating:" + str(book.rating))
            print("Sign Time: " + str(self.libraries[library].signTime))
            print("Books per day: " + str(self.libraries[library].canShipBooksPerDay))
            print("Number of books: " + str(self.libraries[library].nbooks))
            print("\n")
    # ------------------------------------Mutation-----------------------------------
    def hill_climbing(self,num_iterations, log=False):
        iteration = 0
        solution = Solution()
        solution.generate(self)
        # Best solution after 'num_iterations' iterations without improvement
        best_solution = copy.deepcopy(solution) 
        first_score = best_solution.evaluate(self)
        best_score = best_solution.evaluate(self)
        
        print(f"Init Solution:  {best_score}, score: {best_score}")
        time1 = time.time()
        time_start = time1
        print(solution.LibrariesSelected)
        while iteration < num_iterations:
            """if iteration % 1000 == 0:
                time2 = time.time()
                timeExpected = (time2 - time1) * (num_iterations - iteration) / 1000
                print("Iteration: ", timeExpected, " seconds left")
                print("time:",timeExpected/60,"minutes")
                (print(f"Solution:       {iteration}, score: {best_score}"))   
                time1 = time2"""
            iteration += 1
            neighbor_solution = copy.deepcopy(best_solution)
            neighbor_solution.mutation(self)
            neighbor_score = neighbor_solution.evaluate(self)
            #print(f"Solution:       {iteration}, score: {neighbor_score}")
            if neighbor_score > best_score:
                best_solution = neighbor_solution
                best_score = neighbor_score
                if log:
                    (print(f"Solution:       {iteration}, score: {best_score}"))
        #print(f"Final Solution: {best_score}, firstscore: {first_score}")
        print(best_solution.LibrariesSelected)
        if best_solution.checkSolution(self):
            print("Solution is valid")
        else:
            print(best_solution.BooksSelectedByLibrary)
            print(best_solution.LibrariesSelected)
            print("Solution is invalid")
            return False
        print("time elapsed:",(time.time()-time_start),"seconds")
        print("solution:",best_score)
        return best_solution
    
    # ------------------------------------Tabu Search-----------------------------------    
    def tabu_search(self,max_iterations):
        iteration = 0
        stagnation_threshold = 5
        stagnation_count = 0
        tabu_tenure = 10
        neighborhood_size = 10
        solution = Solution()
        solution.generate(self)
        best_solution = copy.deepcopy(solution)
        best_score = best_solution.evaluate(self)
        initial_score = best_solution.evaluate(self)
        tabu_list = []
        print(f"Solution:", initial_score)
        time1 = time.time()
        while iteration < max_iterations:

            if iteration % (max_iterations - 1) == 0:
                time2 = time.time()
                print(f"Time: {time2 - time1}")
                print(f"Solution: {iteration}, score: {best_score}")
                time1 = time2

            iteration += 1
            neighbors_list = []
            
            for i in range(neighborhood_size):
                neighbor_solution = copy.deepcopy(best_solution)
                neighbor_solution.mutation(self)
                neighbors_list.append(neighbor_solution)

            # Best neighbor
            best_neighbor = None
            best_neighbor_score = -1
            for neighbor in neighbors_list:
                neighbor_score = neighbor.evaluate(self)
                if neighbor not in [item[0] for item in tabu_list] or neighbor_score > best_score:
                    if neighbor_score > best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score

            if best_neighbor is None:
                print("No valid neighbors")
                intensified_solution = copy.deepcopy(best_solution)
                for _ in range(neighborhood_size):
                    intensified_solution.mutation(self)
                best_neighbor = intensified_solution
                best_neighbor_score = best_neighbor.evaluate(self)

            # Update best solution
            if best_neighbor_score > best_score:
                best_solution = best_neighbor
                best_score = best_neighbor_score
                tabu_list.append((best_neighbor, tabu_tenure))
                tabu_tenure = max(5, tabu_tenure - 1) 
                stagnation_count = 0
            else:
                stagnation_count += 1
                if stagnation_count >= stagnation_threshold:
                    tabu_tenure = min(20, tabu_tenure + 2)

             # Update and shorten tabu list
            for i in range(len(tabu_list) - 1, -1, -1): 
                tabu_list[i] = (tabu_list[i][0], tabu_list[i][1] - 1) 
                if tabu_list[i][1] <= 0:
                    tabu_list.pop(i)


        if solution.checkSolution(self):
            print("Solution is valid")

        #--------------------------------------------------------------------------------


def test():
    tests = ["a_example.txt","b_read_on.txt","c_incunabula.txt","d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]
    f = open("./tests/result1.txt", "a")
    f.write("Hill Climbing with random\n")
    for test in tests:
        print(test)
        result = 0
        n = 3
        errors = 0
        for i in range(n):
            time1 = time.time()
            manager =DataManager(test)
            result1 =  manager.hill_climbing(1000, False)
            if not result1:
                f.write("Error in test\n")
                errors += 1
            else:
                result += result1.evaluate(manager)/n
        f.write(test + " " + str(result) + "\n")
        f.write("time elapsed: " + str((time.time()-time1)/n) + " seconds\n")
        f.write("errors: " + str(errors) + "\n")
        print("errors: ",errors)
    f.close()
def testCrossover(manager):
    print("Test Crossover")
    n = 70
    initialSolution = Solution()
    initialSolution.generate(manager)
    for i in range(n):
        print(i)
        s = Solution()
        s.generate(manager)
        initialSolution.singlepoint_crossover(manager,s)
        initialSolution.mutation(manager)
    if not initialSolution.checkSolution(manager):
        print("Solution is invalid")
        return False
    else:
        print("Solution is valid")
        return True
def testAll():
    tests = ["a_example.txt","b_read_on.txt","c_incunabula.txt","d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]
    for i in tests:
        print(i)
        manager = DataManager(i)
        if not testCrossover(manager):
            print("Error in test")
            return False
    print("All tests passed")

if __name__ == "__main__":
    test()
    testAll()
    """manager = DataManager("b_read_on.txt")
    solution =Solution()
    solution.generate(manager)
    for i in np.arange(100000):
        print(i)
        solution.mutation(manager)
        if i%1000 == 0:
            if not solution.checkSolution(manager):
                print(solution.LibrariesSelected)
                print(solution.BooksSelectedByLibrary)
                break
    """
    """manager = DataManager("b_read_on.txt")
    manager.tabu_search(50)
    manager.hill_climbing(250)"""
