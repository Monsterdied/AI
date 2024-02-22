#!/usr/bin/env python3

class Book:
    def __init__(self, rating, book_id):
        self.rating = rating
        self.book_id = book_id

    def __hash__(self):
        return hash((self.rating,self.book_id))

    def __eq__(self, other):
        return self.book_id == other.book_id
books = {}
books.add(Book(100,1))
books.add(Book(80,2))
books.add(Book(200,3))
books.add(Book(100,4))
print(books)