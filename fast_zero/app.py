from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routes import auth, todos, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

fake_db = []  # Banco de dados falso


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olar mundo!'}
