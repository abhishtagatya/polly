from .base import Base

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class CommonResponse(Base):
    __tablename__ = "common_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    lang_code: Mapped[str] = mapped_column(String(2))
    event_name: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f'(CommonResponse: {self.id}, {self.lang_code}, {self.event_name})'
