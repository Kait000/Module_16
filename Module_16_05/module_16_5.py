from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

#  для swagger отключаем Try It Out
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})
#  указываем папку шаблонов для Jinja2
templates = Jinja2Templates(directory="templates")
#  сисок объектов пользователей
users = []


class User(BaseModel):
    id: int = None
    username: str = Field(min_length=5, max_length=20, description='Введите имя')
    age: int = Field(ge=18, le=120, description='Введите возраст')


@app.get('/', response_class=HTMLResponse)
async def get_main_page(request: Request) -> HTMLResponse:
    """Возвращает список users"""
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    """Возвращает свойства объекта User"""
    for i in users:
        if i.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': i})
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int) -> User:
    """Удаляет запись с индексом {user_id}"""
    for i in range(len(users)):
        if users[i].id == user_id:
            del_user = users.pop(i)
            return del_user
    raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}', response_model=User)
async def post_user(new_users: User) -> User:
    """
    Добавляет запись: Имя: {username}, возраст: {age}
    - {username} - длина имени от 5 до 20 символов
    - {age} - от 18 до 120
    """
    new_id = max((i.id for i in users), default=0) + 1
    new_users.id = new_id
    users.append(new_users)
    return new_users


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(replace_user: User) -> User:
    """
    Обновляет запись с индексом {user_id}, значениями 'Имя: {username}, возраст: {age}'
    - {username} - длина имени от 5 до 20 символов
    - {age} - от 18 до 120
    """
    for i in users:
        if i.id == replace_user.id:
            i.username = replace_user.username
            i.age = replace_user.age
            return replace_user
    raise HTTPException(status_code=404, detail='User was not found')
