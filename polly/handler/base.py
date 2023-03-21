import logging

from polly.inject import ClientContainer


class BaseHandler:

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        self.client = client
        self.openai_api = self.client.openai_api
        self.db = self.client.database
        self.cache = self.client.cache
        self.logger = logger
