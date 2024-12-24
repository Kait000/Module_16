from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root_page() -> str:
    return "Главная страница"


@app.get('/user/admin')
async def admin_page() -> str:
    return "Вы вошли как администратор"


@app.get('/user/{user_id}')
async def user_page_id(user_id: int) -> str:
    return f"Вы вошли как пользователь № {user_id}"


@app.get('/user/')
async def user_page(username: str, age: int) -> str:
    return f"Информация о пользователе. Имя: '{username}', Возраст: {age}."
