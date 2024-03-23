import numpy as np
from numpy import random
from book import Book
class Solution:
    def __init__(self):
        #List ordered by signup time
        self.LibrariesSelected = np.array([],dtype=int)
        # {LibraryId: [BookId1, BookId2, ...], ...} where the books are the books selected by the library
        self.BooksSelectedByLibrary = {}


    def reshuffleBooksFromLibrary(self,library_id,manager,daysLeft):
        library = manager.libraries[library_id]
        remainingBooks =  daysLeft* library.canShipBooksPerDay
        newBooks = np.array([],dtype=int)
        books = library.books
        books = random.shuffle(books)
        for book in library.books:
            if remainingBooks == 0:
                break
            newBooks=np.append(newBooks,book)
            remainingBooks -= 1
        self.BooksSelectedByLibrary[library_id] = newBooks


    def FillLibrarieWithBooksOrResize(self,library_id,manager,daysLeft):
        NewNbooks = daysLeft * manager.libraries[library_id].canShipBooksPerDay
        try:
            OldNbooks = len(self.BooksSelectedByLibrary[library_id])
        except:
            self.BooksSelectedByLibrary[library_id] = np.array([],dtype=int)
            OldNbooks = 0
        print("LibraryId: ",library_id)
        print("OldNbooks: ",OldNbooks," NewNbooks: ",NewNbooks)
        #crop random books if the list is too big
        if OldNbooks > NewNbooks:
            tmpList = self.BooksSelectedByLibrary[library_id]
            random.shuffle(tmpList)
            self.BooksSelectedByLibrary[library_id] = tmpList[:NewNbooks]
        #add random books if the list is too small
        if OldNbooks < NewNbooks:
            randomized_books =  manager.libraries[library_id].books
            for book in randomized_books:
                if not book in self.BooksSelectedByLibrary[library_id]:
                    self.BooksSelectedByLibrary[library_id] = np.append(self.BooksSelectedByLibrary[library_id],book)


    def FillWithRandomLibraries(self,manager,DaysLeft):
        libraries_ids = np.arange(0,len(manager.libraries))
        DaysLeft = manager.nDays
        while DaysLeft>0 and len(libraries_ids) > 0:
            library_id = random.choice(libraries_ids)
            library = manager.libraries[library_id]
            if DaysLeft-library.signTime >=0 and library_id not in self.LibrariesSelected:
                DaysLeft = DaysLeft - library.signTime
                self.LibrariesSelected = np.append(library_id,self.LibrariesSelected)
                self.BooksSelectedByLibrary[library_id] = np.array([])
                self.reshuffleBooksFromLibrary(library_id,manager,DaysLeft)
            # remove from the possible to add to the list of libraries
            libraries_ids = np.delete(libraries_ids,np.where(libraries_ids == library_id))
    
    def checkSolution(self,manager):
        #check if the solution is valid
        #check if the libraries selected are in the list of libraries
        for library in self.LibrariesSelected:
            if library not in manager.libraries:
                print("Library not in the list of libraries")
                return False
        #check if the books selected are in the list of books
        for library in self.BooksSelectedByLibrary.keys():
            for book in self.BooksSelectedByLibrary[library]:
                try:
                    manager.books[book]
                except:
                    print("Book not in the list of books")
                    return False
        #check if the books selected are in the list of books of the library
        for library in self.BooksSelectedByLibrary:
            for book in self.BooksSelectedByLibrary[library]:
                found = False
                for book_id in manager.libraries[library].books:
                    if book_id == book:
                        found = True
                        break
                if not found:
                    print("Book not in the list of books of the library")
                    return False
        libraries = set()
        for library in self.BooksSelectedByLibrary:
            if library in libraries:
                print("Library is repeated")
                return False
            libraries.add(library)
        # check if libraries and daysLeft are the same
        days_tmp = 0
        for library in self.LibrariesSelected:
            days_tmp += manager.libraries[library].signTime
        if days_tmp > manager.nDays:
            print("number total of days is less than the sum of the days of the libraries")
            print("Days left is incorrect")
            return False
        new_days = manager.nDays
        for library in self.LibrariesSelected:
            booksSelected = self.BooksSelectedByLibrary[library]
            new_days -= manager.libraries[library].signTime
            nbooks = len(booksSelected)
            if nbooks > new_days*manager.libraries[library].canShipBooksPerDay:
                print(nbooks,str(new_days*manager.libraries[library].canShipBooksPerDay))
                print("Number of books doesnt match the days left and the books per day of the library")
                return False
        return True

    def generate(self,manager):
        #select 
        self.FillWithRandomLibraries(manager,manager.nDays)

    def evaluate(self,manager):
        score = 0
        books = set()
        for books1 in self.BooksSelectedByLibrary.values():
            for book_id in books1:
                if book_id not in books:
                    score += manager.books[book_id]
                    books.add(book_id)
        return score
    def mutate_swap_order(self,manager):
        #swap two libraries
        if len(self.LibrariesSelected) < 2:
            return
        i = random.randint(0,len(self.LibrariesSelected))
        j = random.randint(0,len(self.LibrariesSelected))
        while i == j:
            j = random.randint(0,len(self.LibrariesSelected))
        daysLeft = manager.nDays
        recalculate = False
        for library_index in np.arange(0,len(self.LibrariesSelected)):
            library_id = self.LibrariesSelected[library_index]
            if i == library_index or j == library_index:
                new_library_id = self.LibrariesSelected[j] if i == library_index else self.LibrariesSelected[i]
                daysLeft -= manager.libraries[new_library_id].signTime
                print("library_id:",library_index,"days left:",daysLeft)
                self.FillLibrarieWithBooksOrResize(new_library_id,manager,daysLeft)
                recalculate = True
            else:
                daysLeft -= manager.libraries[library_id].signTime
                if recalculate:
                    self.FillLibrarieWithBooksOrResize(library_id,manager,daysLeft)
            if i < library_index and j < library_index:
                break
        print(self.BooksSelectedByLibrary)
        self.LibrariesSelected[i],self.LibrariesSelected[j] = self.LibrariesSelected[j],self.LibrariesSelected[i]
    def mutation(self,manager):
        #r = random.rand(0,3)
        r=0
        if r == 0:
            #self.mutate_swap_libraries(manager)
        #elif r == 1:
            self.mutate_swap_order(manager)

    def mutate_swap_libraries(self,manager):
        #swap two libraries
        i = random.randint(0,len(self.LibrariesSelected))
        libraries = np.arange(0,len(manager.libraries))
        found = False
        library_id_j = -1
        tries = 0
        while not found and tries < 1000 and len(libraries) > 0:
            library_id_j = random.choice(libraries)
            if library_id_j not in self.LibrariesSelected:
                found = True
                break
            libraries = np.delete(libraries,np.where(libraries == library_id_j))
            tries += 1
        if library_id_j == -1:
            print("Error: No Suitable Library Found")
            print("Tries: ",tries)
            return
        
        daysLeft = manager.nDays
        recalculate = False
        size_of_libraries = len(self.LibrariesSelected)
        for library_index in np.arange(len(self.LibrariesSelected)):  
            library_id = self.LibrariesSelected[library_index]
            if i == library_index:
                daysLeft -= manager.libraries[library_id_j].signTime
                recalculate = True
                # if the library is the last one and sometimes if the days left get negative it cant be added
                if daysLeft > 0:
                    self.FillLibrarieWithBooksOrResize(library_id_j,manager,daysLeft)
                else:
                    return
            else:
                daysLeft -= manager.libraries[library_id].signTime
                if recalculate:
                    if daysLeft > 0:
                        size_of_libraries = library_index
                        break
                    self.FillLibrarieWithBooksOrResize(library_id,manager,daysLeft)
        if size_of_libraries < len(self.LibrariesSelected):
            for library_id in self.LibrariesSelected[size_of_libraries:]:
                self.BooksSelectedByLibrary.pop(library_id)
            self.LibrariesSelected = self.LibrariesSelected[:size_of_libraries]
        self.LibrariesSelected[i] = library_id_j
    def crossover(self,manager,solution2):
        return #future implementation