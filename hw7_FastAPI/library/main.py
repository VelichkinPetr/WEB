
# 1. Книги библиотеки

# Данные: книги библиотеки.
# для типизации можно воспользоваться TypedDict | NamedTuple
# id: int
# title: str author: str
# year: int | None = None
# in_stock: bool = True (в наличии: да/нет)

# Добавить фильтрацию: GET /books?in_stock=true|false.
#       если in_stock передается в параметре запроса:
#           то надо вернуть все книги: у которых in_stock=true|false
#       иначе: маршрут должен вернуть просто список всех книг

# Добавить маршрут DELETE /books - удалить все книги.

from typing import Any, Dict
from model import Book
from library import Library, LibraryService
from fastapi import FastAPI, status

app = FastAPI()

@app.post('/books', status_code=status.HTTP_200_OK)
def create_book(data: Dict) -> Dict:
    return library.add_book(data)

@app.get('/books', status_code = status.HTTP_200_OK)
def get_books(in_stock: bool = None) -> Dict[str, list]:
    return {
            'data':library.get_books(in_stock)
           }

@app.get('/books/{id}', status_code = status.HTTP_200_OK)
def get_book(id: int) -> Dict[str, Any]:
    return library.get_book_by_id(id)

@app.put('/books/{id}', status_code = status.HTTP_200_OK)
def update_book(id: int, data: Dict[str, Any]):
    return library.update_book(id, data)

@app.delete('/books', status_code = status.HTTP_200_OK)
def delete_books():
    library.delete_all_books()

@app.delete('/book/{id}', status_code = status.HTTP_200_OK)
def delete_book(id: int):
    library.delete_book_by_id(id)

books_db: list[Book] = [
    Book(
        id=1,
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        in_stock=True
    ),
    Book(
        id=2,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1966,
        in_stock=False
    ),
    Book(
        id=3,
        title="1984",
        author="Джордж Оруэлл",
        year=1949,
        in_stock=True
    )
]
service = LibraryService(books_db)
library = Library(service)
