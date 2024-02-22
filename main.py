
import Library
class DataManager:    
    def __init__(self,filename):
        self.filename = filename
        self.books = {}
        file1 = open(filename, 'r')
        line = file1.readline()
        self.read_data_info(line)
        line = file1.readline()
        self.read_data_info(line)
        line = file1.readline()
        libraryId = 0
        while line:
            data = line.split(' ')
            nbooks = int(data[0])
            signTime = int(data[1])
            canShipBooksPerDay = int(data[2])
            line = file1.readline()
            data = line.split(' ')
            books = {}
            i = 0
            for rating in data:
                books[i] = rating
                i += 1
            if i != nbooks:
                print("Error in reading book rating\nNumber of books read is not equal to the number of books mentioned in the file rating")
            self.books[libraryId] = Library(nbooks,signTime,canShipBooksPerDay,books)
            libraryId += 1
            line = file1.readline()
            
            
            

    def read_data_info(self,line):
        data = line.split(' ')
        self.nBooks = int(data[0])
        self.nLibraries = int(data[1])
        self.nDays = int(data[2])
    def read_book_rating(self,line):
        data = line.split(' ')
        self.books = {}
        i = 0
        for rating in data:
            self.books[i] = rating
            i += 1
        if i != self.nBooks:
            print("Error in reading book rating\nNumber of books read is not equal to the number of books mentioned in the file rating")
            
