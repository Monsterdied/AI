import numpy as np
from numpy import random
class Solution:
    def __init__(self):
        #List ordered by signup time
        self.LibrariesSelected = []
        # {LibraryId: ([BookId1, BookId2, ...],daysLeft), ...} where the books are the books selected by the library
        self.BooksSelectedByLibrary = {}
        self.UsedBooks = set()
        self.currScore = 0

    def generate(self,manager):
        #select 
        libraries_ids = np.arange(len(manager.libraries))
        NumberTotalOfdays = manager.nDays
        CurrentDaysUsed = 0
        while(len(self.UsedBooks) < len(manager.books) and len(libraries_ids)>0 and NumberTotalOfdays > CurrentDaysUsed):
            library_id = random.choice(libraries_ids)
            library = manager.libraries[library_id]
            if library.signTime + CurrentDaysUsed <= NumberTotalOfdays:
                CurrentDaysUsed += library.signTime
                daysLeft = NumberTotalOfdays - CurrentDaysUsed
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
    def evaluate(self,manager):
        return self.currScore
    
    def mutation(self,manager):
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
            PossibleLibraries = manager.signTimeToLibraries[old_library.signTime]
            library_id = -1
            while len(PossibleLibraries) > 1 and not found_match:
                library_id= random.choice(PossibleLibraries)
                if library_id not in self.LibrariesSelected:
                    found_match = True
                PossibleLibraries.remove(library_id)
            mutations += 1
        if library_id == -1:
            #print("No possible library to swap")
            return
        #remove the library from the list of libraries
        self.LibrariesSelected[library_index] = library_id

        (usedBooksLibrary,daysLeft) = self.BooksSelectedByLibrary[old_library_id]
        #remove the books from the list of books
        old_books_score = 0
        for book in usedBooksLibrary:
            self.UsedBooks.remove(book)
            old_books_score +=manager.books[book]
        remainingBooks = daysLeft * manager.libraries[library_id].canShipBooksPerDay
        newBooks = []
        new_book_rating = 0
        for book in manager.libraries[library_id].books:
            if remainingBooks == 0:
                break
            if book not in self.UsedBooks:
                new_book_rating+=book.rating
                self.UsedBooks.add(book)
                newBooks.append(book)
                remainingBooks -= 1
        #update currScore
        self.currScore += new_book_rating-old_books_score
        #add the books to the list of books selected by the library
        del self.BooksSelectedByLibrary[old_library_id]
        self.BooksSelectedByLibrary[library_id] = (newBooks,daysLeft)

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
