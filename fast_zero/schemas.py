"""Os schemas fazem a validação dos dados usando Pydantic"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    """Representação do usuários no DB fake"""

    id: int


class UserPublic(BaseModel):
    """Não retorna a senha do usuário na response"""

    id: int
    username: str
    email: EmailStr

    # Altera o comportamento de model_validate
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    """Retorna uma lista com todos os usuários, porém sem suas senhas"""

    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Esse schema será utilizado para tipificar os dados
    extraídos do token JWT e garantir que temos um campo
    username que será usado para identificar o usuário.
    """

    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    created_at: datetime
    updated_at: datetime
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
