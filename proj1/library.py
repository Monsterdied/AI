class Library: 
    # methods 
    def __init__(self, BookNumber, signTime,BooksPerDay,books): 
        self.nbooks = BookNumber
        self.signTime = signTime
        self.canShipBooksPerDay =BooksPerDay
        self.books = books