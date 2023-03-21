import logging

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.inject import ClientContainer


class VoiceMessageHandler(BaseHandler):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)

    async def voice_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        common_response = self.common_response_uc.get_common_response_by_filter('IMPLEMENT_ERROR')
        await update.message.reply_text(text=common_response.message)
