import datetime

from .base import Base

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_message: Mapped[str] = mapped_column(Text)
    chat_response: Mapped[str] = mapped_column(Text)
    common_response: Mapped[bool] = mapped_column(Boolean)
    primary_lang: Mapped[str] = mapped_column(String(2))
    learning_lang: Mapped[str] = mapped_column(String(2))
    created_at: Mapped[datetime.datetime]
    user_id: Mapped[int] = mapped_column(Integer)
