from .base import Base

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    messaging_lang: Mapped[str] = mapped_column(String(2))
    primary_lang: Mapped[str] = mapped_column(String(2))
    learning_lang: Mapped[str] = mapped_column(String(2))

    def __repr__(self):
        return f'(User: {self.id}, {self.name}, {self.messaging_lang})'