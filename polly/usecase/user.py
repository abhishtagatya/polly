import logging

import openai
import redis
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .base import UseCase
from ..model.user import User


class UserUC(UseCase):
    GET_USER_INFO_KEY = "users:{id}"
    GET_USER_INFO_VALUE = "{name}:{primary_lang}:{learning_lang}"

    DAY_EXPIRE = 60 * 60 * 24

    def __init__(self, openai_api: openai.api_base, db: sqlalchemy.Engine, cache: redis.Redis, logger: logging.Logger):
        super().__init__(openai_api, db, cache, logger)

    def create_or_update_user(self, uid: int, name: str, username: str, messaging_lang: str, primary_lang: str,
                              learning_lang: str) -> None:
        with Session(self.db) as session:
            statement = insert(User).values(id=uid, name=name, username=username, messaging_lang=messaging_lang)
            statement = statement.on_conflict_do_update(
                constraint='users_pk',
                set_={
                    'name': name,
                    'username': username,
                    'messaging_lang': messaging_lang,
                    'primary_lang': primary_lang,
                    'learning_lang': learning_lang
                }
            )
            session.execute(statement)
            session.commit()

    def get_user_by_id(self, uid: int) -> User:
        result = self.cache.get(self.GET_USER_INFO_KEY.format(id=uid))
        if result is not None:
            u_name, u_primary_lang, u_learning_lang = result.decode('utf-8').split(':')
            return User(
                id=uid, name=u_name, primary_lang=u_primary_lang, learning_lang=u_learning_lang
            )

        with Session(self.db) as session:
            result = session.query(User).filter(User.id == uid).first()

            self.cache.set(
                self.GET_USER_INFO_KEY.format(id=uid),
                self.GET_USER_INFO_VALUE.format(
                    name=result.name,
                    primary_lang=result.primary_lang,
                    learning_lang=result.learning_lang
                )
            )
            self.cache.expire(
                self.GET_USER_INFO_KEY.format(id=uid),
                self.DAY_EXPIRE
            )

            return result
