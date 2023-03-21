from typing import Dict
import logging

import openai
import sqlalchemy
import redis
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram.ext import Application


class BaseEngine:

    def __init__(self,
                 telegram_token: str,
                 openai_token: str,
                 database_uri: str,
                 redis_cred: tuple):
        self._telegram_token = telegram_token
        self._openai_token = openai_token
        self._database_uri = database_uri
        self._redis_host, self._redis_port, self._redis_pass = redis_cred

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

        self.telegram_api = Application.builder().token(self._telegram_token).build()
        openai.api_key = self._openai_token
        self.openapi_api = openai
        self.db = sqlalchemy.create_engine(self._database_uri, echo=True)
        self.redis = redis.Redis(
            host=self._redis_host,
            port=self._redis_port,
            password=self._redis_pass
        )

    def run(self):
        self.telegram_api.run_polling()

    @classmethod
    def from_dict(cls, config: Dict):
        """
        Load configuration from dictionary
        :param config: Dict
        :return: Instance
        """

        if config is None:
            raise ValueError('Config cannot be empty or null')

        telegram_token = config.get('TELEGRAM_TOKEN', '')
        if telegram_token == '':
            raise ValueError('Config key `TELEGRAM_TOKEN` cannot be empty.')

        openai_token = config.get('OPENAI_TOKEN', '')
        if openai_token == '':
            raise ValueError('Config key `OPENAI_TOKEN` cannot be empty.')

        database_uri = config.get('DATABASE_URI', '')
        if database_uri == '':
            raise ValueError('Config key `DATABASE_URI` cannot be empty.')

        redis_cred = (
            config.get('REDIS_HOST', ''),
            config.get('REDIS_PORT', ''),
            config.get('REDIS_PASSWORD', '')
        )

        return cls(
            telegram_token=telegram_token,
            openai_token=openai_token,
            database_uri=database_uri,
            redis_cred=redis_cred
        )
