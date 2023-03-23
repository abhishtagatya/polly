import logging
from io import BytesIO, FileIO

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.voice import VoiceUC
from polly.inject import ClientContainer


class VoiceMessageHandler(BaseHandler):

    SIZE_LIMIT = 50000

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)
        self.voice_uc = VoiceUC(client, logger)

    async def voice_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        tg_audio_file = await update.message.voice.get_file()
        if tg_audio_file.file_size > self.SIZE_LIMIT:
            common_response = self.common_response_uc.get_common_response_by_filter('VOICE_LENGTH_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        user_message = await self.voice_uc.get_voice_message(uid=user.id, file=tg_audio_file)

        if user_message == '':
            common_response = self.common_response_uc.get_common_response_by_filter('VOICE_PROCESS_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        voice_message_file = await self.voice_uc.create_voice_message(
            text=user_message, lang=found_user.learning_lang, uid=found_user.id
        )

        await update.message.reply_voice(voice=voice_message_file, caption=f'Polly heard you say "{user_message}"')
