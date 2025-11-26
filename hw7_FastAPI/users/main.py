# 2. Пользователи и их профили
#
# Данные: список пользователей.
#
#     username: str
#     email: str
#     full_name: str | None = None
#     is_active: bool = True
#
# Добавить проверку, чтобы username был уникален (если уже есть — вернуть 400).
# Добавить маршрут GET /users/by-username/{username}.

from typing import Any, Dict
from model import User
from users import Users, UsersService
from fastapi import FastAPI, status

app = FastAPI()

@app.post('/users', status_code=status.HTTP_200_OK)
def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    return users.add_user(data)

@app.get('/users', status_code = status.HTTP_200_OK)
def get_users(in_stock: bool = None) -> Dict[str, list]:
    return {
            'data':users.get_users(in_stock)
           }

@app.get('/users/by-username/{username}', status_code = status.HTTP_200_OK)
def get_user(username: str) -> Dict[str, Any]:
    return users.get_user_by_username(username)

@app.put('/users/by-username/{username}', status_code = status.HTTP_200_OK)
def update_user(username: str, data: Dict[str, Any]):
    return users.update_user(username, data)

@app.delete('/users', status_code = status.HTTP_200_OK)
def delete_users():
    users.delete_all_users()

@app.delete('/users/by-username/{username}', status_code = status.HTTP_200_OK)
def delete_user(username: str):
    users.delete_user_by_username(username)

users_db: list[User] = [
    User(
        username="ivan_petrov",
        email="ivan@example.com",
        full_name="Иван Петров",
        is_active=True
    ),
    User(
        username="anna_sidorova",
        email="anna@example.com",
        full_name="Анна Сидорова",
        is_active=False
    ),
    User(
        username="alex_volkov",
        email="alex@example.com"
    )
]
service = UsersService(users_db)
users = Users(service)
