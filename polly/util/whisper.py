import openai
from io import FileIO

class Whisper:
    def __init__(self, api_key: str, model_name='whisper-1'):
        self.api_key = api_key
        self.model_name = model_name
        openai.api_key = api_key

    def preprocessing(self, audio_file: FileIO) -> bytes:
        pass 

    def transcribe(self, audio_file: FileIO) -> str:
        response = openai.Audio.transcribe(
            model=self.model_name,
            file=audio_file
        )
        return response['text']
