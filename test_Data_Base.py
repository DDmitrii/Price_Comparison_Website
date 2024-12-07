import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Base import DataBase, Book, Genre, Author  # Замените your_module на имя вашего файла


def test_add_book():
    db = DataBase(db_url='sqlite:///:memory:')

    book = Book(name="Атлант расправил плечи", price=39.99, link="http://example.com", image_link="http://example.com/image.jpg",
                website_name="Bookstore")

    db.add_book(book, genres=["Fantasy"], authors=["J.K. Rowling"])

    assert db.get_book_by_name(book_name="Атлант расправил плечи")[0] is not None
    assert db.get_book_by_name(book_name="Атлант расправил плечи")[0].name == book.name
    assert db.get_book_by_name(book_name="Атлант расправил плечи")[0].authors[0].name == 'J.K. Rowling'

    db.delete_book("Атлант расправил плечи")


def test_get_book_by_name():
    db = DataBase(db_url='sqlite:///:memory:')

    book_name = "Атлант расправил плечи"

    book = Book(name="Атлант расправил плечи", price=39.99, link="http://example.com",
                image_link="http://example.com/image.jpg",
                website_name="Bookstore")

    db.add_book(book, genres=["Fantasy"], authors=["J.K. Rowling"])

    books = db.get_book_by_name(book_name)

    assert len(books) > 0
    assert books[0].name == book_name

    db.delete_book(book_name)


def test_delete_book():
    db = DataBase(db_url='sqlite:///:memory:')

    book_name = "Harry Potter"

    db.delete_book(book_name)

    assert db.all_target_table("books") == []


def test_get_book_by_genre():
    db = DataBase(db_url='sqlite:///:memory:')

    genre_name = "Comedy"

    book_name = "Funny Book"

    book = Book(name=book_name, price=39.99, link="http://example.com",
                image_link="http://example.com/image.jpg",
                website_name="Bookstore")

    db.add_book(book, genres=[genre_name], authors=["Dm"])

    assert db.get_books_by_genre(genre_name)[0].name == book_name

    db.delete_book(book_name)


def test_get_book_by_authors():
    db = DataBase(db_url='sqlite:///:memory:')

    author_name = "Pushkin"

    book_name = "Tales"

    book = Book(name=book_name, price=39.99, link="http://example.com",
                image_link="http://example.com/image.jpg",
                website_name="Bookstore")

    db.add_book(book, genres=["Fantasy"], authors=[author_name])

    assert db.get_books_by_author(author_name)[0].name == book_name

    db.delete_book(book_name)


if __name__ == "__main__":
    pytest.main()