from typing import Dict
import logging

from polly.inject import ClientContainer


class BaseBot:

    def __init__(self, config: Dict):

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.client = ClientContainer.load(config)

    def run(self):
        self.client.telegram_api.run_polling()
