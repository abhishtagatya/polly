import logging

from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.prompt_instruction import PromptInstruction
from polly.inject import ClientContainer


class PromptInstructionUC(UseCase):

    GET_PROMPT_INSTRUCTION_CACHE_KEY = 'chat:{instruction_code}'

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

    def get_prompt_instruction_by_filter(self, instruction_code: str) -> PromptInstruction:

        result = self.cache.get(self.GET_PROMPT_INSTRUCTION_CACHE_KEY.format(instruction_code=instruction_code))
        if result is not None:
            return PromptInstruction(instruction_code=instruction_code, prompt=result)

        with Session(self.db) as session:
            result = session.query(PromptInstruction).filter(
                PromptInstruction.instruction_code == instruction_code
            ).first()

            # Update Cache
            self.cache.set(self.GET_PROMPT_INSTRUCTION_CACHE_KEY.format(
                instruction_code=instruction_code), result.prompt)

            return result
