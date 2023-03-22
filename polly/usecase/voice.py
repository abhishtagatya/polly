import logging

import telegram
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.conversation import Conversation
from polly.util.whisper import Whisper
from polly.inject import ClientContainer


class VoiceUC(UseCase):

    ORIGINAL_PATH = 'temp/{user_id}.ogg'
    EXPORT_PATH = 'temp/{user_id}.mp3'

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

        self.openai_whisper = Whisper(client=self.client.openai_api)

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
