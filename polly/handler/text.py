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
from ..usecase.conversation import ConversationUC


class TextMessageHandler(BaseHandler):

    def __init__(self,
                 openai_api: openai.api_base,
                 db: sqlalchemy.Engine,
                 cache: redis.Redis,
                 logger: logging.Logger):
        super().__init__(openai_api, db, cache, logger)
        self.common_response_uc = CommonResponseUC(openai_api, db, cache, logger)
        self.user_uc = UserUC(openai_api, db, cache, logger)
        self.conversation_uc = ConversationUC(openai_api, db, cache, logger)

    async def text_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Send message on any text message """

        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        common_response = self.common_response_uc.get_common_response_by_filter('IMPLEMENT_ERROR')
        self.conversation_uc.update_conversation(
            user_message=update.message.text,
            chat_response=common_response.message,
            user_id=found_user.id,
            primary_lang=found_user.primary_lang,
            learning_lang=found_user.learning_lang
        )
        await update.message.reply_text(text=common_response.message)