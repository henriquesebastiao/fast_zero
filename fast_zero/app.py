from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routes import auth, todos, users
from fast_zero.schemas import Message

description = """
Esta API foi desenvolvida durante o curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/)
#### Documentação mais legível: [Redoc](https://api.henriquesebastiao.com/redoc)
"""

app = FastAPI(
    title='FastAPI do Zero',
    version='dev',
    docs_url='/',
    description=description,
    contact={
        'name': 'Henrique Sebastião',
        'email': 'contato@henriquesebastiao.com',
        'url': 'https://github.com/henriquesebastiao',
    },
)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

fake_db = []  # Banco de dados falso


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olar mundo!'}
