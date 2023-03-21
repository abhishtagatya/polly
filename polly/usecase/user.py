import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.user import User
from polly.inject import ClientContainer


class UserUC(UseCase):
    GET_USER_INFO_KEY = "users:{id}"
    GET_USER_INFO_VALUE = "{name}:{primary_lang}:{learning_lang}"

    DAY_EXPIRE = 60 * 60 * 24

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

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

            self.cache.set(
                self.GET_USER_INFO_KEY.format(id=uid),
                self.GET_USER_INFO_VALUE.format(
                    name=name,
                    primary_lang=primary_lang,
                    learning_lang=learning_lang
                ),
                ttl=self.cache.ONE_WEEK
            )

            session.commit()

    def get_user_by_id(self, uid: int) -> User:
        result = self.cache.get(self.GET_USER_INFO_KEY.format(id=uid))
        if result is not None:
            u_name, u_primary_lang, u_learning_lang = result.split(':')
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
                ),
                ttl=self.cache.ONE_WEEK
            )

            return result
