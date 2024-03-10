from numpy import random
class Solution:
    def __init__(self):
        #List ordered by signup time
        self.LibrariesSelected = []
        # {LibraryId: ([BookId1, BookId2, ...],daysLeft), ...} where the books are the books selected by the library
        self.BooksSelectedByLibrary = []
        self.UsedBooks = {}
        self.currScore = 0
    def mutation(self,manager):
        #select a random library
        found_match = False
        mutations = 0
        while not found_match and mutations < 1000:
            library_id = random.randint(len(manager.libraries))
            old_library_id = random.randint(0,len(self.LibrariesSelected ))
            if library_id not in self.LibrariesSelected:
                found_match = True
            mutations += 1
        
        #remove the library from the list of libraries
        self.LibrariesSelected[old_library_id] = library_id

        (usedBooksLibrary,daysLeft) = self.UsedBookslibrary[old_library_id]
        #remove the books from the list of books
        for book in usedBooksLibrary:
            manager.books.remove(book)
        del self.UsedBookslibrary[old_library_id]
        remainingBooks = daysLeft * manager.libraries[library_id].canShipBooksPerDay
        for book in manager.libraries[library_id].books:
            if remainingBooks == 0:
                break
            if book not in self.UsedBooks:
                self.UsedBooks.add(book.id)
                remainingBooks -= 1
        #add the books to the list of books selected by the library
        self.BooksSelectedByLibrary[library.id] = (library.books,library.signup_days)
