import logging
from io import BytesIO, FileIO

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.voice import VoiceUC
from polly.util.whisper import Whisper
from polly.inject import ClientContainer


class VoiceMessageHandler(BaseHandler):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)
        self.voice_uc = VoiceUC(client, logger)

        self.openai_whisper = Whisper(client=self.client.openai_api)

    async def voice_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user

        tg_audio_file = await update.message.voice.get_file()
        user_message = await self.voice_uc.get_voice_message(uid=user.id, file=tg_audio_file)

        if user_message == '':
            common_response = self.common_response_uc.get_common_response_by_filter('VOICE_ERROR')
            await update.message.reply_text(text=common_response.message)

        await update.message.reply_text(text=user_message)
