import logging

import openai
import redis
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .base import UseCase
from ..model.conversation import Conversation


class ConversationUC(UseCase):

    def __init__(self, openai_api: openai.api_base, db: sqlalchemy.Engine, cache: redis.Redis, logger: logging.Logger):
        super().__init__(openai_api, db, cache, logger)

    def update_conversation(self,
                            user_message: str,
                            chat_response: str,
                            primary_lang: str,
                            learning_lang: str,
                            user_id: int,
                            common_response: bool = False):
        with Session(self.db) as session:
            statement = insert(Conversation).values(
                user_message=user_message,
                chat_response=chat_response,
                primary_lang=primary_lang,
                learning_lang=learning_lang,
                user_id=user_id,
                common_response=common_response
            )
            session.execute(statement)
            session.commit()
