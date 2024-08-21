from fastapi import FastAPI

from fast_zero.routes import auth, todos, users

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
