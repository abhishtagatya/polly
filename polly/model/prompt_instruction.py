from .base import Base

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class PromptInstruction(Base):
    __tablename__ = "prompt_instructions"

    id: Mapped[int] = mapped_column(primary_key=True)
    instruction_code: Mapped[str] = mapped_column(String(20))
    prompt: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f'(PromptInstruction: {self.id}, {self.instruction_code})'
