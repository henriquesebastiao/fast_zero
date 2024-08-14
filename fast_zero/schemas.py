"""Os schemas fazem a validação dos dados usando Pydantic"""

from pydantic import BaseModel, EmailStr


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


class UserList(BaseModel):
    """Retorna uma lista com todos os usuários, porém sem suas senhas"""

    users: list[UserPublic]
