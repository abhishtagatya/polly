from typing import Dict

import openai


class OpenAIClient:

    WHISPER_KEY = 'OPENAI_WHISPER'
    GPT_KEY = 'OPENAI_GPT'

    def __init__(self, token: str, model_dict: Dict):
        self._token = token
        self._model_dict = model_dict

        openai.api_key = self._token
        self.openai_api = openai
        self.openai_model = model_dict

    def __call__(self, *args, **kwargs):
        return self.openai_api
    