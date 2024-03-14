
from library import Library
from book import Book
from solution import Solution
from sortedcontainers import SortedList
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
        
        while iteration < num_iterations:
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
        print(solution.checkSolution(self))
        return best_solution

if __name__ == "__main__":
    manager =DataManager("e_so_many_books.txt")
    #manager.hill_climbing(100, True)
    #print(manager.signTimeToLibraries[16])
    #print(manager.libraries[5].books.sum())
    #print(manager.libraries[94].books.sum())
    s = Solution()
    s.generate(manager)
    print(s.LibrariesSelected)
    s.mutation(manager)
    print(s.LibrariesSelected)

    #newSolution = manager.hill_climbing(100, True)
    #print(newSolution.BooksSelectedByLibrary.keys())
    #print(newSolution)
    #manager.print_libraries()
            
