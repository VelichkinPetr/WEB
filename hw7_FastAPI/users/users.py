from __future__ import annotations
from typing import Any, Dict
from model import User
from fastapi  import HTTPException, status


class Users:

    def __init__(self, service: UsersService):
        self.__service = service

    def add_user(self, data: Dict) -> Dict[str, Any]:
        return self.__service.add_user(data)
    
    def get_users(self, is_active: bool = None) -> Dict[str, Any]:
        return self.__service.get_users(is_active)
    
    def get_user_by_username(self, username: str) -> Dict[str, Any]:
        return self.__service.get_user_by_username(username)
    
    def update_user(self, username: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.__service.update_user_by_username(username, data)
    
    def delete_all_users(self):
        self.__service.delete_all_users()
    
    def delete_user_by_username(self, username: str):
        self.__service.delete_book_by_username(username)

class UsersService:

    def __init__(self, storage: list):
        self.storage = storage
    
    def add_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'username' in data.keys():
            if self.search_user_index_by_username(data['username']) is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Such a user already exists')
        if ({'username', 'email'} & data.keys()) != {'username', 'email'}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Missing data for create')
        new_user = User(**data)
        self.storage.append(new_user)
        return new_user.model_dump()
    
    def get_users(self, is_active: bool = None) -> list[User]:
        if is_active is None:
             return self.storage
        return [user for user in self.storage if user.is_active == is_active]
    
    def get_user_by_username(self, username: str) -> list[User]:
        target_index = self.search_user_index_by_username(username)
        if target_index is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='User with username not found')
        return self.storage[target_index].model_dump()

    def update_user_by_username(self, username: str, data: Dict[str, Any]) -> Dict[str, Any]:
        target_index = self.search_user_index_by_username(username)

        if 'username' in data.keys():
            if self.search_user_index_by_username(data['username']) is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Such a user already exists')

        if target_index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with username not found')
        
        common_user = self.storage[target_index].model_dump()
        common_keys = common_user.keys() & data.keys()
        if common_keys:
            update_data = {key: data[key] for key in common_keys}
            updated_user = self.storage[target_index].model_copy(update=update_data)
            self.storage[target_index] = updated_user
            return updated_user
        
    def delete_all_users(self) -> None:
        self.storage.clear()

    def delete_book_by_username(self, username: str) -> None:
        target_index = self.search_user_index_by_username(username)
        if target_index is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='User with username  not found')
        del self.storage[target_index]
            
    def search_user_index_by_username(self, username: str) -> int | None:
        for i, user in enumerate(self.storage):
            if user.username == username:
                return i
        return None
