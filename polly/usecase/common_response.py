import logging

import openai
import redis
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.common_response import CommonResponse


class CommonResponseUC(UseCase):

    GET_COMMON_RESPONSE_CACHE_KEY = 'chat:{event_name}:{lang_code}'

    def __init__(self, openai_api: openai.api_base, db: sqlalchemy.Engine, cache: redis.Redis, logger: logging.Logger):
        super().__init__(openai_api, db, cache, logger)

    def get_common_response_by_filter(self, event_name: str, lang_code: str = 'EN') -> CommonResponse:

        result = self.cache.get(self.GET_COMMON_RESPONSE_CACHE_KEY.format(event_name=event_name, lang_code=lang_code))
        if result is not None:
            return CommonResponse(event_name=event_name, lang_code=lang_code, message=result.decode('utf-8'))

        with Session(self.db) as session:
            result = session.query(CommonResponse).filter(
                CommonResponse.lang_code == lang_code
            ).filter(
                CommonResponse.event_name == event_name
            ).first()

            # Update Cache
            self.cache.set(self.GET_COMMON_RESPONSE_CACHE_KEY.format(
                event_name=event_name,
                lang_code=lang_code), result.message)

            return result
