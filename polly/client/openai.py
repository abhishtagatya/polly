import openai


class OpenAIClient:

    def __init__(self, token: str):
        self._token = token
        openai.api_key = self._token
        self.openai_api = openai

    def __call__(self, *args, **kwargs):
        return self.openai_api
    