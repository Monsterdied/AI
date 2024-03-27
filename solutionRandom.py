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
        #print("LibraryId: ",library_id)
        #print("Remaining Books: ",remainingBooks)
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
        #print("NewNbooks:",NewNbooks)
        #print("Nbooks:",NewNbooks)
        #try:
        OldNbooks = len(self.BooksSelectedByLibrary[library_id])
        #except:
        #    self.BooksSelectedByLibrary[library_id] = np.array([],dtype=int)
        #    OldNbooks = 0
        #print("LibraryId: ",library_id)
        #print("OldNbooks: ",OldNbooks," NewNbooks: ",NewNbooks)
        #crop random books if the list is too big
        if OldNbooks > NewNbooks:
            tmpList = self.BooksSelectedByLibrary[library_id]
            random.shuffle(tmpList)
            #print("Size of list cropped:",len(tmpList[:NewNbooks]))
            self.BooksSelectedByLibrary[library_id] = tmpList[:NewNbooks]
        #add random books if the list is too small
        if OldNbooks < NewNbooks:
            randomized_books =  manager.libraries[library_id].books
            addedBooksNumber = NewNbooks - OldNbooks
            for book in randomized_books:
                if addedBooksNumber == 0:
                    break
                if not book in self.BooksSelectedByLibrary[library_id]:
                    self.BooksSelectedByLibrary[library_id] = np.append(self.BooksSelectedByLibrary[library_id],book)
                    addedBooksNumber -= 1
        #print("LibraryId: ",library_id)
        #print("Books: ",len(self.BooksSelectedByLibrary[library_id]))


    def FillWithRandomLibraries(self,manager,DaysLeft):
        libraries_ids = np.arange(0,len(manager.libraries))
        DaysLeft = manager.nDays
        while DaysLeft>0 and len(libraries_ids) > 0:
            library_id = random.choice(libraries_ids)
            library = manager.libraries[library_id]
            if DaysLeft-library.signTime >=0 and library_id not in self.LibrariesSelected:
                DaysLeft = DaysLeft - library.signTime
                self.LibrariesSelected = np.append(self.LibrariesSelected,library_id)
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
        for library in self.BooksSelectedByLibrary.keys():
            if not library in self.LibrariesSelected:
                print( "Library:",library," not in the selected list!!!!\n")
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
                print("Library_id",str(library))
                print("It is ",nbooks,"Should Be ",str(new_days*manager.libraries[library].canShipBooksPerDay))
                print("Number of books doesnt match the days left and the books per day of the library")
                return False
        return True

    def generate(self,manager):
        #select 
        self.FillWithRandomLibraries(manager,manager.nDays)

    def evaluate(self,manager):
        score = 0
        books = set()
        for library in self.LibrariesSelected:

            for book_id in self.BooksSelectedByLibrary[library]:
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
                #print("library_id:",new_library_id,"days left:",daysLeft)
                self.FillLibrarieWithBooksOrResize(new_library_id,manager,daysLeft)
                recalculate = True
            else:
                daysLeft -= manager.libraries[library_id].signTime
                if recalculate:
                    self.FillLibrarieWithBooksOrResize(library_id,manager,daysLeft)
            if i < library_index and j < library_index:
                break
        #print(self.BooksSelectedByLibrary)
        self.LibrariesSelected[i],self.LibrariesSelected[j] = self.LibrariesSelected[j],self.LibrariesSelected[i]
    def mutation(self,manager):
        r = random.randint(0,3)
        if r == 0:
            self.mutate_swap_libraries(manager)
        elif r == 1:
            self.mutate_swap_order(manager)
        elif r == 2:
            self.mutate_shuffle_some_books(manager)

    def mutate_swap_libraries(self,manager):
        #swap two libraries
        i = random.randint(0,len(self.LibrariesSelected))
        libraries = np.arange(0,len(manager.libraries))
        found = False
        library_id_j = -1
        tries = 0
        while not found and tries < 1000 and len(libraries) > 0:
            library_id_tmp = random.choice(libraries)
            if library_id_tmp not in self.LibrariesSelected:
                library_id_j = library_id_tmp
                found = True
                break
            libraries = np.delete(libraries,np.where(libraries == library_id_tmp))
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
                    self.BooksSelectedByLibrary.pop(library_id)
                    self.BooksSelectedByLibrary[library_id_j] = np.array([],dtype=int)
                    self.FillLibrarieWithBooksOrResize(library_id_j,manager,daysLeft)
                else:
                    return
            else:
                daysLeft -= manager.libraries[library_id].signTime
                if recalculate:
                    if daysLeft < 0:
                        size_of_libraries = library_index
                        break
                    self.FillLibrarieWithBooksOrResize(library_id,manager,daysLeft)
        if size_of_libraries < len(self.LibrariesSelected):
            for library_id in self.LibrariesSelected[size_of_libraries:]:
                self.BooksSelectedByLibrary.pop(library_id)
            self.LibrariesSelected = self.LibrariesSelected[:size_of_libraries]
        self.LibrariesSelected[i] = library_id_j
    def singlepoint_crossover(self,manager,solution):
        middle_days = manager.nDays//2
        counter_day1 = 0
        libraries1 = np.array([],dtype=int)
        tmp_book_libraries1 = {}
        for library in self.LibrariesSelected:
            counter_day1 += manager.libraries[library].signTime
            if counter_day1 > middle_days:
                counter_day1 -= manager.libraries[library].signTime
                break
            try:
                tmp_book_libraries1[library] = self.BooksSelectedByLibrary[library]
            except:
                tmp_book_libraries1[library] = np.array([],dtype=int)
            libraries1 = np.append(libraries1,library)
        self.BooksSelectedByLibrary = tmp_book_libraries1
        libraries2 = np.array([],dtype=int)
        counter_day2 = counter_day1
        for library in solution.LibrariesSelected[::-1]:
            counter_day2 += manager.libraries[library].signTime
            if counter_day2 > manager.nDays:
                break
            if library not in libraries1:
                libraries2 = np.append(libraries2,library)
                self.BooksSelectedByLibrary[library] = solution.BooksSelectedByLibrary[library]
        libraries2 = libraries2[::-1]
        for i in libraries2:
            counter_day1 += manager.libraries[i].signTime
            self.FillLibrarieWithBooksOrResize(i,manager,manager.nDays - counter_day1)
        self.LibrariesSelected = np.append(libraries1 ,libraries2)
        return #future implementation
    def mutate_shuffle_some_books(self,manager):
        #get a random number of libraries
        nLibraries = random.randint(0,len(self.LibrariesSelected))
        library_ids = np.array([],dtype=int)
        #shuffle some books
        #print("Libraries:",nLibraries)
        for i in np.arange(0,nLibraries):
            library_id = random.choice(self.LibrariesSelected)
            library_ids = np.append(library_ids,library_id)
        leftDays = manager.nDays
        for library_id in self.LibrariesSelected:
            leftDays -= manager.libraries[library_id].signTime
            #print("LibraryId: ",library_id,"DaysLeft: ",leftDays,"nBooks :",leftDays*manager.libraries[library_id].canShipBooksPerDay)
            if library_id in library_ids:

                self.reshuffleBooksFromLibrary(library_id,manager,leftDays)