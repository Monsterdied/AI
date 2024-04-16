from sortedcontainers import SortedSet
class Book:
    def __init__(self, rating, book_id):
        self.rating = rating
        self.book_id = book_id

    def __hash__(self):
        return hash(self.book_id)

    def __eq__(self, other):
        return self.book_id == other.book_id
    def __lt__(self, other):
        return self.rating > other.rating
    def __str__(self) -> str:
        return "id:" + str(self.book_id) + " rating:" + str(self.rating)
    
if __name__ == "__main__":
    books = SortedSet()
    books.add(Book(100,1))
    books.add(Book(80,2))
    books.add(Book(200,3))
    books.add(Book(100,4))
    for book in books:
        print("id:" + str(book.book_id) + " rating:" + str(book.rating))