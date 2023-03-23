import logging

import telegram

from polly.usecase.base import UseCase
from polly.util.whisper import Whisper
from polly.util.google_tts import GoogleTTS
from polly.inject import ClientContainer


class VoiceUC(UseCase):

    ORIGINAL_PATH = 'temp/{user_id}.ogg'
    EXPORT_PATH = 'temp/{user_id}.mp3'
    SYNTH_PATH = 'temp/bot-{user_id}.ogg'

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

        self.openai_whisper = Whisper(client=self.client.openai_api)
        self.gcloud_tts = GoogleTTS(client=self.client.gcloud_api)

    async def get_voice_message(self, uid: int, file: telegram.File) -> str:
        await file.download_to_drive(custom_path=self.ORIGINAL_PATH.format(user_id=uid))

        await self.openai_whisper.convert_audio(
            self.ORIGINAL_PATH.format(user_id=uid),
            self.EXPORT_PATH.format(user_id=uid)
        )

        with open(self.EXPORT_PATH.format(user_id=uid), 'rb') as audio_file:
            response = self.openai_whisper.transcribe(
                audio_file=audio_file
            )

        return response.get('text', '')

    async def create_voice_message(self, uid: int, text: str, lang: str) -> str:
        out_file = self.SYNTH_PATH.format(user_id=uid)
        self.gcloud_tts.synthesize(
            text=text, lang=lang, out_file=self.SYNTH_PATH.format(user_id=uid)
        )

        return out_file
