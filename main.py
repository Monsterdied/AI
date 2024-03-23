
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
        time_start = time1
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
            neighbor_score = neighbor_solution.currScore 
            if neighbor_score > best_score:
                best_solution = neighbor_solution
                best_score = neighbor_score
                if log:
                    (print(f"Solution:       {iteration}, score: {best_score}"))
        print(f"Final Solution: {best_score}, firstscore: {first_score}")
        if best_solution.checkSolution(self):
            print("Solution is valid")
        else:
            print("Solution is invalid")
            return False
        print("time elapsed:",(time.time()-time_start),"seconds")
        return best_solution
def test():
    tests = ["a_example.txt","b_read_on.txt","c_incunabula.txt","d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]
    f = open("./tests/result.txt", "a")
    f.write("Hill Climbing\n")
    for test in tests:
        print(test)
        result = 0
        n = 3
        for i in range(n):
            manager =DataManager(test)
            result += manager.hill_climbing(2000, False).currScore/n
        f.write(test + " " + str(result) + "\n")
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
    tests = ["b_read_on.txt","c_incunabula.txt","d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]
    for i in tests:
        print(i)
        manager = DataManager(i)
        if not testCrossover(manager):
            print("Error in test")
            return False
if __name__ == "__main__":
    testAll()
    #print(manager.signTimeToLibraries[16])
    #print(manager.libraries[5].books.sum())
    #print(manager.libraries[94].books.sum())
    #s = Solution()
    #s.generate(manager)
    #s.mutation(manager)
    #s.checkSolution(manager)

    #newSolution = manager.hill_climbing(100, True)
    #print(newSolution.BooksSelectedByLibrary.keys())
    #print(newSolution)
    #manager.print_libraries()
            
