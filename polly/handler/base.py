import logging

import openai
import redis
import sqlalchemy


class BaseHandler:

    def __init__(self, openai_api: openai.api_base, db: sqlalchemy.Engine, cache: redis.Redis, logger: logging.Logger):
        self.openai_api = openai_api
        self.db = db
        self.cache = cache
        self.logger = logger
