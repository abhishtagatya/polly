from typing import Dict, Tuple

from polly.client.cache import CacheClient
from polly.client.database import DatabaseClient
from polly.client.openai import OpenAIClient
from polly.client.telegram import TelegramClient


class ClientContainer:

    def __init__(self,
                 telegram_token: str,
                 openai_token: str,
                 openai_model: Dict,
                 database_uri: str,
                 redis_cred: Tuple,
                 ):
        self._telegram_token = telegram_token
        self._openai_token = openai_token
        self._openai_model = openai_model
        self._database_uri = database_uri
        self._redis_host, self._redis_port, self._redis_pass = redis_cred

        self.telegram_api = TelegramClient(token=self._telegram_token).__call__()
        self.openai_api = OpenAIClient(token=self._openai_token, model_dict=self._openai_model)
        self.database = DatabaseClient(database_uri=self._database_uri).__call__()
        self.cache = CacheClient(host=self._redis_host, port=self._redis_port, password=self._redis_pass)

    @classmethod
    def load(cls, config: Dict):
        """
        Load configuration from dictionary
        :param config:
        :return:
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

        openai_model = {
            'OPENAI_WHISPER': config.get('OPENAI_WHISPER', ''),
            'OPENAI_GPT': config.get('OPENAI_GPT')
        }

        return cls(
            telegram_token=telegram_token,
            openai_token=openai_token,
            openai_model=openai_model,
            database_uri=database_uri,
            redis_cred=redis_cred
        )
