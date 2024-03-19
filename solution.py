import numpy as np
from numpy import random
from book import Book
class Solution:
    def __init__(self):
        #List ordered by signup time
        self.LibrariesSelected = []
        # {LibraryId: ([BookId1, BookId2, ...],daysLeft), ...} where the books are the books selected by the library
        self.BooksSelectedByLibrary = {}
        self.UsedBooks = set()
        self.currScore = 0

    def FillWithRandomLibraries(self,manager,DaysLeft):
        libraries_ids = np.arange(len(manager.libraries))
        CurrentDaysUsed = 0
        while(len(self.UsedBooks) < len(manager.books) and len(libraries_ids)>0 and DaysLeft>0):
            library_id = random.choice(libraries_ids)
            library = manager.libraries[library_id]
            if library.signTime + CurrentDaysUsed <= DaysLeft and library_id not in self.LibrariesSelected:
                CurrentDaysUsed += library.signTime
                daysLeft = DaysLeft - CurrentDaysUsed
                self.LibrariesSelected.append(library_id)
                remainingBooks =  daysLeft* library.canShipBooksPerDay
                newBooks = []
                new_books_rating = 0
                for book in library.books:
                    if remainingBooks == 0:
                        break
                    if book.book_id not in self.UsedBooks:
                        new_books_rating+=book.rating
                        self.UsedBooks.add(book.book_id)
                        newBooks.append(book.book_id)
                        remainingBooks -= 1
                self.BooksSelectedByLibrary[library_id] = (newBooks,daysLeft)
                self.currScore += new_books_rating
            # remove from the possible to add to the list of libraries
            libraries_ids = np.delete(libraries_ids,np.where(libraries_ids == library_id))
    def generate(self,manager):
        #select 
        self.FillWithRandomLibraries(manager,manager.nDays)

    def evaluate(self,manager):
        return self.currScore
    
    def checkSolution(self,manager):
        #check if the solution is valid
        #check if the libraries selected are in the list of libraries
        for library in self.LibrariesSelected:
            if library not in manager.libraries:
                print("Library not in the list of libraries")
                return False
        #check if the books selected are in the list of books
        for library in self.BooksSelectedByLibrary.keys():
            for book in self.BooksSelectedByLibrary[library][0]:
                try:
                    manager.books[book]
                except:
                    print("Book not in the list of books")
                    return False
        #check if the days left are correct
        for library in self.BooksSelectedByLibrary:
            if self.BooksSelectedByLibrary[library][1] < 0:
                print("Days left is negative")
                return False
        #check if the books selected are in the list of books of the library
        for library in self.BooksSelectedByLibrary:
            for book in self.BooksSelectedByLibrary[library][0]:
                found = False
                for i in manager.libraries[library].books:
                    if i.book_id == book:
                        found = True
                        break
                if not found:
                    print("Book not in the list of books of the library")
                    return False
        # check score
        value = 0
        for library in self.BooksSelectedByLibrary:
            for book in self.BooksSelectedByLibrary[library][0]:
                value += manager.books[book]
        if value != self.currScore:
            print("CurrScore is different from the sum of the books")
            return False
        books = set()
        # check if the books are repeated
        for library in self.BooksSelectedByLibrary:
            for book in self.BooksSelectedByLibrary[library][0]:
                if book in books:
                    print("Book is repeated")
                    return False
                books.add(book)
        # check if the libraries are repeated
        libraries = set()
        for library in self.BooksSelectedByLibrary:
            if library in libraries:
                print("Library is repeated")
                return False
            libraries.add(library)
        # check if libraries and daysLeft are the same
        days_tmp = 0
        for library in self.BooksSelectedByLibrary:
            days_tmp += manager.libraries[library].signTime
        if days_tmp > manager.nDays:
            print("Days left is incorrect")
            return False
        return True
    
    def mutation(self,manager):
        r = random.randint(0,2)
        if r == 0:
            self.mutation_swap_exact(manager)
        else:
            self.mutation_swap_order(manager)
        
    def mutation_swap_order(self,manager):
        #select a random library
        found_match = False
        #find libraries with the same signTime
        #optimizar esta parte no futuro-----------------------------------------------------
        #---------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------
        library_index_1 = random.randint(len(self.LibrariesSelected))
        library_id_1 = self.LibrariesSelected[library_index_1]
        #libraries with the same signTime as the old one
        while not found_match:
            library_index_2= random.choice(len(self.LibrariesSelected))
            if(library_index_1 != library_index_2):
                library_id_2 = self.LibrariesSelected[library_index_2]
                found_match = True
        daysLeft = manager.nDays
        #remove books from used books
        currvalue = self.currScore
        for i in self.BooksSelectedByLibrary[library_id_1][0]:
            self.UsedBooks.remove(i)
            currvalue -= manager.books[i]
        for i in self.BooksSelectedByLibrary[library_id_2][0]:
            self.UsedBooks.remove(i)
            currvalue -= manager.books[i]
        for i in np.arange(len(self.LibrariesSelected)):
            if i == library_index_1 or i == library_index_2:
                if(library_index_1 == i):
                    new_library_id = library_id_2
                else:
                    new_library_id = library_id_1
                new_books = []
                new_library = manager.libraries[new_library_id]
                daysLeft -= new_library.signTime
                n_books = daysLeft*new_library.canShipBooksPerDay
                for book in new_library.books:
                    if n_books == 0:
                        break
                    n_books -= 1
                    if book.book_id not in self.UsedBooks:
                        new_books.append(book.book_id)
                        self.UsedBooks.add(book.book_id)
                        currvalue += book.rating
                self.BooksSelectedByLibrary[new_library_id] = (new_books,daysLeft)
            else:
                library_tmp_id = self.LibrariesSelected[i]
                library_tmp = manager.libraries[library_tmp_id] 
                daysLeft -= library_tmp.signTime
                (old_books,old) = self.BooksSelectedByLibrary[library_tmp_id]
                #if the days left are different from the previous days left we need to recalculate the selected books
                if old != daysLeft:
                    new_books = []
                    n_books = daysLeft*library_tmp.canShipBooksPerDay
                    #remove the old books from the used books because they can be used or not have time to be used
                    for i in old_books:
                        self.UsedBooks.remove(i)
                    for book in library_tmp.books:
                        if n_books == 0:
                            break
                        n_books -= 1
                        if book.book_id not in self.UsedBooks:
                            new_books.append(book.book_id)
                            self.UsedBooks.add(book.book_id)
                            currvalue += book.rating
                    self.BooksSelectedByLibrary[library_tmp_id] = (new_books,daysLeft)
        #remove the books from the list of books
        self.currScore = currvalue
    def mutation_swap_exact(self,manager):
        #select a random library
        found_match = False
        mutations = 0
        #find libraries with the same signTime
        #optimizar esta parte no futuro-----------------------------------------------------
        #---------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------
        while not found_match and mutations < 1000:
            library_index = random.randint(len(self.LibrariesSelected))
            old_library_id = self.LibrariesSelected[library_index]
            old_library = manager.libraries[old_library_id]
            #libraries with the same signTime as the old one
            library_id = -1
            possible_signdays = np.arange(1,old_library.signTime+1)
            while not found_match and len(possible_signdays)>0:
                curr_signTime = random.choice(possible_signdays)
                possible_signdays = np.delete(possible_signdays,np.where(possible_signdays == curr_signTime))
                PossibleLibraries = manager.signTimeToLibraries[curr_signTime]
                curr_signTime -= 1
                while len(PossibleLibraries) > 1 and not found_match:
                    library_id_tmp= random.choice(PossibleLibraries)
                    if library_id_tmp not in self.LibrariesSelected:
                        library_id = library_id_tmp
                        found_match = True
                    PossibleLibraries.remove(library_id_tmp)
            mutations += 1
        if library_id == -1:
            print("No possible library to swap")
            return
        #remove the library from the list of libraries
        daysLeft = manager.nDays
        reCalculate = False
        for i in range(len(self.LibrariesSelected)):
            library_id_tmp = self.LibrariesSelected[i]
            (old_books,old) = self.BooksSelectedByLibrary[library_id_tmp]
            if i == library_index:
                reCalculate = True
                daysLeft -= manager.libraries[library_id].signTime
                self.LibrariesSelected[i] = library_id
                self.BooksSelectedByLibrary.pop(library_id_tmp)
                library_id_tmp = library_id
            else:
                daysLeft -= manager.libraries[library_id_tmp].signTime
            if reCalculate:
                new_books = []
                n_books = daysLeft*manager.libraries[library_id_tmp].canShipBooksPerDay
                for j in old_books:
                    self.UsedBooks.remove(j)
                    self.currScore -= manager.books[j]
                for book in manager.libraries[library_id_tmp].books:
                    if n_books == 0:
                        break
                    n_books -= 1
                    if book.book_id not in self.UsedBooks:
                        new_books.append(book.book_id)
                        self.UsedBooks.add(book.book_id)
                        self.currScore += book.rating
                
                self.BooksSelectedByLibrary[library_id_tmp] = (new_books,daysLeft)
        self.FillWithRandomLibraries(manager,daysLeft)

    def __str__(self) -> str:
        output = "Libraries Selected: " + str(self.LibrariesSelected) + "\n"
        for i in self.LibrariesSelected:
            (books,daysLeft) = self.BooksSelectedByLibrary[i]
            output+= "Library: " + str(i) + "\n"
            output+="Days Left: " + str(daysLeft) + "\n"
            output+="Books: " + "\n"
            for book in books:
                output+=str(book) + " "
            output+="\n\n"
        return output + "Score: " + str(self.currScore) + "\n"
