from __future__ import annotations
from typing import Any, Dict
from model import Book
from fastapi  import HTTPException, status


class Library:

    def __init__(self, service: LibraryService):
        self.__service = service

    def add_book(self, data: Dict) -> Book:
        return self.__service.add_book(data)
    
    def get_books(self, in_stock: bool = None) -> Dict[str, Any]:
        return self.__service.get_books(in_stock)
    
    def get_book_by_id(self, id: int) -> Dict[str, Any]:
        return self.__service.get_book_by_id(id)
    
    def update_book(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.__service.update_book_by_id(id, data)
    
    def delete_all_books(self):
        self.__service.delete_all_books()
    
    def delete_book_by_id(self, id: int):
        self.__service.delete_book_by_id(id)

class LibraryService:

    def __init__(self, storage: list):
        self.storage = storage
        self.max_id = max([book.id for book in self.storage]) + 1
        self.id = 1 if self.storage == [] else self.max_id
    
    def add_book(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if ({'title', 'author'} & data.keys()) != {'title', 'author'}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Missing data for create')
        
        data['id'] = self.id
        new_book = Book(**data)
        self.storage.append(new_book)
        self.id += 1
        return new_book.model_dump()
    
    def get_books(self, in_stock: bool = None) -> list[Book]:
        if in_stock is None:
             return self.storage
        return [book for book in self.storage if book.in_stock == in_stock]
    
    def get_book_by_id(self, id: int) -> list[Book]:
        target_index = self.search_book_index_by_id(id)
        if target_index is not None:
             return self.storage[target_index].model_dump()
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Book with id not found')

    def update_book_by_id(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        target_index = self.search_book_index_by_id(id)
        if target_index is not None:
            common_book = self.storage[target_index].model_dump()
            common_keys = common_book.keys() & data.keys() - {'id'}
            if common_keys:
                update_data = {key: data[key] for key in common_keys}
                updated_book = self.storage[target_index].model_copy(update=update_data)
                self.storage[target_index] = updated_book
                return updated_book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book with id not found')

    def delete_all_books(self) -> None:
        self.storage.clear()

    def delete_book_by_id(self, id: int) -> None:
        target_index = self.search_book_index_by_id(id)
        if target_index is not None:
            del self.storage[target_index]
            return
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Book with id not found')
    
    def search_book_index_by_id(self, id: int) -> int | None:
        for i, book in enumerate(self.storage):
            if book.id == id:
                return i
        return None
