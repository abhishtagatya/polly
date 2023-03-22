import openai
from io import FileIO

class Whisper:
    def __init__(self, client: openai, model_name='whisper-1'):
        self.client = client
        self.model_name = model_name

    def preprocessing(self, audio_file: FileIO) -> bytes:
        # Preprocessing?
        pass 

    def transcribe(self, audio_file: FileIO) -> str:
        response = self.client.Audio.transcribe(
            model=self.model_name,
            file=audio_file
        )
        return response['text']
