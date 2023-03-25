import logging
from typing import List, Dict

import telegram

from polly.model.user import User
from polly.usecase.base import UseCase
from polly.util.chatgpt import ChatGPT
from polly.util.google_tts import GoogleTTS
from polly.inject import ClientContainer


class TextUC(UseCase):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

        self.openai_gpt = ChatGPT(client=self.client.openai_api)

    async def get_chat_answer(self,
                              past_message: List,
                              new_message: str,
                              prompt: str,
                              instruction: Dict):
        full_prompt = prompt.format(
            user_name=instruction['USER_NAME'],
            primary_lang=instruction['PRIMARY_LANG'],
            learning_lang=instruction['LEARNING_LANG']
        )

        response = self.openai_gpt.chat(
            system_message=full_prompt,
            past_message=past_message,
            new_message=new_message
        )

        return response['choices'][0]['message']['content']


