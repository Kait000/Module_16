from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_users() -> dict:
    """Возвращает словарь users"""
    return users


@app.post('/user/{username}/{age}')
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                  description='Введите имя')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст')]) -> str:
    """
    Добавляет в словарь запись: Имя: {username}, возраст: {age}
    - {username} - длина имени от 5 до 20 символов
    - {age} - от 18 до 120
    """
    current_index = str(int(max(users, key=int)) + 1)
    users[current_index] = f'Имя: {username}, возраст: {age}'
    return f"User {current_index} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(description='Введите user_id')],
                      username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Введите имя')],
                      age: Annotated[int, Path(ge=18, le=120, description='Введите возраст')]) -> str:
    """
    Обновляет запись в словаре с индексом {user_id}, значениями 'Имя: {username}, возраст: {age}'
    - {username} - длина имени от 5 до 20 символов
    - {age} - от 18 до 120
    """
    for key in users:
        if key == str(user_id):
            users[key] = f'Имя: {username}, возраст: {age}'
            return f'The user {user_id} is updated'
    raise HTTPException(status_code=404, detail=f'Запись с user_id = {user_id} не найдена!')


@app.delete('/user/{user_id}')
async def delete__user(user_id: Annotated[int, Path(description='Введите user_id')]) -> str:
    """Удаляет запись из словаря с индексом {user_id}"""
    for key in users:
        if key == str(user_id):
            users.pop(key)
            return f'User {user_id} has been deleted'
    raise HTTPException(status_code=404, detail=f'Запись с user_id = {user_id} не найдена!')
