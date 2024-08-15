from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,  # Vai escolher o tipo ideal de dado no DB
    mapped_column,  # Passar propriedades SQL para a tabela
    registry,  # Para registrar os metadados das tabelas
)

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
