import logging
from enum import Enum

import openai
import redis
import sqlalchemy
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, ConversationHandler

from .base import BaseHandler
from ..usecase.user import UserUC
from ..usecase.common_response import CommonResponseUC


class VoiceMessageHandler(BaseHandler):

    def __init__(self,
                 openai_api: openai.api_base,
                 db: sqlalchemy.Engine,
                 cache: redis.Redis,
                 logger: logging.Logger):
        super().__init__(openai_api, db, cache, logger)
        self.common_response_uc = CommonResponseUC(openai_api, db, cache, logger)
        self.user_uc = UserUC(openai_api, db, cache, logger)

    async def voice_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        common_response = self.common_response_uc.get_common_response_by_filter('IMPLEMENT_ERROR')
        await update.message.reply_text(text=common_response.message)
