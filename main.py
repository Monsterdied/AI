
from library import Library
from book import Book
from solution import Solution
from sortedcontainers import SortedList
import time
import copy
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
            line2 = file1.readline()
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
        books = self.books
        LibraryBooks = SortedList()
        i = 0
        for bookid in bookIds:# pode se alterar o ordered set para lista la a frente é so necessario ordenar mas para ja vamos tentar assim
            LibraryBooks.add(Book(self.books[int(bookid)],int(bookid)))
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
        first_score = best_solution.currScore
        best_score = best_solution.currScore
        
        print(f"Init Solution:  {best_score}, score: {best_score}")
        time1 = time.time()
        while iteration < num_iterations:
            if iteration % 1000 == 0:
                time2 = time.time()
                timeExpected = (time2 - time1) * (num_iterations - iteration) / 1000
                print("Iteration: ", timeExpected, " seconds left")
                print("time:",timeExpected/60,"minutes")
                (print(f"Solution:       {iteration}, score: {best_score}"))   
                time1 = time2
            iteration += 1
            neighbor_solution = copy.deepcopy(best_solution)
            neighbor_solution.mutation(self)
            neighbor_score = neighbor_solution.currScore 
            if neighbor_score > best_score:
                best_solution = neighbor_solution
                best_score = neighbor_score
                if log:
                    (print(f"Solution:       {iteration}, score: {best_score}"))   
        print(f"Final Solution: {best_score}, firstscore: {first_score}")
        if solution.checkSolution(self):
            print("Solution is valid")
        else:
            print("Solution is invalid")
        return best_solution
    # ------------------------------------Tabu Search-----------------------------------
    def tabu_search(self,max_interations,tabu_list_size,neighborhood_size):
        iteration = 0
        solution = Solution()
        solution.generate(self)
        best_solution = copy.deepcopy(solution)
        best_score = best_solution.currScore
        tabu_list = []
        print(f"Solution:", best_score)
        time1 = time.time()
        while iteration < max_interations:

            if iteration % (max_interations-1) == 0:
                time2 = time.time()
                print (f"Time: {time2 - time1}" )
                (print(f"Solution:       {iteration}, score: {best_score}"))   
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
                if neighbor not in tabu_list:
                    neighbor_score = neighbor.currScore
                    if neighbor_score > best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score

            # If no neighbor is valid
            if best_neighbor is None:
                neighbors_list = []
                for i in range(neighborhood_size):
                    neighbor_solution = copy.deepcopy(best_solution)
                    neighbor_solution.mutation(self)
                    neighbors_list.append(neighbor_solution)

                best_neighbor = max(neighbors_list, key=lambda x: x.currScore)
                best_neighbor_score = best_neighbor.currScore

            # Update best solution
            if best_neighbor_score > best_score:
                best_solution = best_neighbor
                best_score = best_neighbor_score
                tabu_list.append(best_neighbor)
                if len(tabu_list) > tabu_list_size:
                    tabu_list.pop(0)
        if solution.checkSolution(self):
            print("Solution is valid")
            




if __name__ == "__main__":
    manager =DataManager("b_read_on.txt")
    manager.tabu_search(50, 50, 5)
    manager.hill_climbing(50, True)
            


"""
To do:
Aspiration Criteria: As discussed earlier, you might want to consider adding an aspiration criteria, which would allow a move even if it is tabu, under certain conditions (for example, if the move leads to a solution better than any seen so far).

Termination Criteria: Besides the maximum number of iterations, you might want to consider other termination criteria, such as a time limit or a condition that checks if the solution has not improved for a certain number of iterations.

Tabu Tenure: Instead of always removing the oldest solution from the tabu list when it exceeds its maximum size, you could consider implementing a more sophisticated tabu tenure strategy. For example, you could vary the tenure of a solution based on its quality or the frequency of its components in the search history.

Logging and Result Reporting: You might want to add more logging and result reporting to help you understand the progress and performance of the algorithm. For example, you could log the best solution found in each iteration, the size of the tabu list, the number of neighbors generated, etc. At the end of the search, you could report the best solution found, the total number of iterations, the total running time, etc.

Code Organization and Modularity: To make the code easier to read and maintain, you might want to consider breaking down the tabu search method into smaller methods, each responsible for a specific part of the algorithm (e.g., generating neighbors, selecting the best neighbor, updating the tabu list, etc.).
"""