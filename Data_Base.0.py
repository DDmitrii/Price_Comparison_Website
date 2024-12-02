from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload

Base = declarative_base()

# Промежуточная таблица для связи (многие к многим)
# Book <-> Genre
book_genres = Table(
    "book_genres", Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)

# Промежуточная таблица для связи (многие к многим)
# Book <-> Author
book_authors = Table(
    "book_authors", Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True)
)

# Класс для таблицы книг
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    genres = relationship("Genre", secondary=book_genres, back_populates="books")
    authors = relationship("Author", secondary=book_authors, back_populates="books")

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __repr__(self):
        genres_list = [genre.name for genre in self.genres]
        authors_list = [author.name for author in self.authors]
        return f"Book(id={self.id}, name='{self.name}', price={self.price}, genres={genres_list}, authors={authors_list})"


# Класс для таблицы жанров
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", secondary=book_genres, back_populates="genres")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Genre(id={self.id}, name='{self.name}')"

# Класс для таблицы авторов
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", secondary=book_authors, back_populates="authors")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

# Класс для управления базой данных
class DataBase:
    def __init__(self, db_url="sqlite:///books.db"):
        """
        Инициализация базы данных и создание таблиц.
        """
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_genre(self, session, genre_name: str):
        """
        Добавляет жанр в базу данных если он не существует.
        """
        genre = session.query(Genre).filter(Genre.name.ilike(f"%{genre_name}%")).first()
        if not genre:
            genre = Genre(name=genre_name)
            session.add(genre)
            print(f"Genre '{genre_name}' added.")
        return genre

    def add_author(self, session, author_name: str):
        """
        Добавляет автора в базу данных если он не существует.
        """
        author = session.query(Author).filter(Author.name.ilike(f"%{author_name}%")).first()
        if not author:
            author = Author(name=author_name)
            session.add(author)
            print(f"Author '{author_name}' added.")
        return author
        
    def add_book(self, book: Book, genres: list[str], authors: list[str]):
        """
        Добавляет книгу в базу данных с жанрами и авторами.
        Если книга уже существует, добавляет недостающие жанры и авторов.
        """
        session = self.Session()
        try:
            # Проверка существования книги
            existing_book = session.query(Book).filter(Book.name.ilike(f"%{book.name}%")).first()
            if existing_book:
                print(f"Book '{book.name}' already exists.")
                
                for genre_name in genres:
                    genre = self.add_genre(session, genre_name)
                    if genre not in existing_book.genres:
                        existing_book.genres.append(genre)
                
                for author_name in authors:
                    author = self.add_author(session, author_name)
                    if author not in existing_book.authors:
                        existing_book.authors.append(author)
                session.commit()
                return

            # Если книга не существует, то создаем её с жанрами и авторами
            for genre_name in genres:
                genre = self.add_genre(session, genre_name)
                book.genres.append(genre)

            for author_name in authors:
                author = self.add_author(session, author_name)
                book.authors.append(author)

            session.add(book)
            session.commit()
            print(f"Book '{book.name}' added successfully with genres {genres} and authors {authors}.")
            
        except Exception as e:
            session.rollback()
            print(f"Error adding book: {e}")
        finally:
            session.close()

    def delete_book(self, book_name: str):
        """
        Удаляет книгу по её названию.
        """
        session = self.Session()
        try:
            book_to_delete = session.query(Book).filter(Book.name.ilike(f"%{book_name}%")).first()
            
            if not book_to_delete:
                print(f"Book with name {book_name} not found.")
                return
            
            book_to_delete.genres.clear()
            book_to_delete.authors.clear()

            session.delete(book_to_delete)
            session.commit()
            print(f"Book with name {book_name} deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting book: {e}")
        finally:
            session.close()
    
    def get_book_by_name(self, book_name: str) -> list[Book]:
        """
        Находит книги по названию.
        """
        session = self.Session()
        try:
            books_by_name = (
                session.query(Book)
                .filter(Book.name.ilike(f"%{book_name}%"))
                .options(joinedload(Book.genres), joinedload(Book.authors))
                .all()
            )
            return books_by_name if books_by_name else []
        finally:
            session.close()

    def get_books_by_author(self, author_name: str) -> list[Book]:
        """
        Находит книги по автору.
        """
        session = self.Session()
        try:
            books_by_author = (
                session.query(Book)
                .join(Book.authors)
                .filter(Author.name.ilike(f"%{author_name}%"))
                .options(joinedload(Book.genres), joinedload(Book.authors))
                .all()
            )
            return books_by_author if books_by_author else []
        finally:
            session.close()

    def get_books_by_genre(self, genre_name: str) -> list[Book]:
        """
        Находит книги по жанру.
        """
        session = self.Session()
        try:
            books_by_genre = (
                session.query(Book)
                .join(Book.genres)
                .filter(Genre.name.ilike(f"%{genre_name}%"))
                .options(joinedload(Book.genres), joinedload(Book.authors))
                .all()
            )
            return books_by_genre if books_by_genre else []
        finally:
            session.close()

    def all_targer_table(self, table_name: str) -> list[Book]:
        """
        Возвращает все элемнты данной таблицы из базы данных.
        """
        session = self.Session()
        try:
            match table_name:
                case "books":
                    return (
                        session.query(Book)
                        .options(joinedload(Book.genres), joinedload(Book.authors))
                        .all()
                    )
                case "genres":
                    return (
                        session.query(Genre)
                        .options(joinedload(Genre.books))
                        .all()
                    )
                case "authors":
                    return (
                        session.query(Genre)
                        .options(joinedload(Genre.books))
                        .all()
                    )
                case _:
                    print(f"Table with name {table_name} doesn't exist")
                    return []
        finally:
            session.close()

if __name__ == "__main__":
    # Создаем базу данных
    db = DataBase()