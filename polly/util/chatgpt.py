from enum import Enum
from typing import List

from polly.client.openai import OpenAIClient


class ChatGPT:

    SYSTEM_ROLE = 'system'
    USER_ROLE = 'user'
    ASSISTANT_ROLE = 'assistant'

    def __init__(self, client: OpenAIClient):
        self.client = client.openai_api
        self.model_name = client.openai_model.get(
            client.GPT_KEY
        )

    @staticmethod
    def build_message_chain(
            system_message: str,
            past_message: List,
            new_message: str):
        message_chain = [{'role': ChatGPT.SYSTEM_ROLE, 'content': system_message}]
        for role, message in past_message:
            if role == 'USER':
                message_chain.append({'role': ChatGPT.USER_ROLE, 'content': message})
            else:
                message_chain.append({'role': ChatGPT.ASSISTANT_ROLE, 'content': message})
        message_chain.append({'role': ChatGPT.USER_ROLE, 'content': new_message})
        return message_chain

    def chat(self,
             system_message: str,
             past_message: List,
             new_message: str):
        message_chain = self.build_message_chain(
            system_message, past_message, new_message
        )
        response = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=message_chain,
        )
        return response
