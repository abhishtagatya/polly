import logging

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.conversation import ConversationUC
from polly.inject import ClientContainer


class TextMessageHandler(BaseHandler):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)
        self.conversation_uc = ConversationUC(client, logger)

    async def text_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Send message on any text message """

        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        common_response = self.common_response_uc.get_common_response_by_filter('IMPLEMENT_ERROR')
        self.conversation_uc.update_conversation(
            user_message=update.message.text,
            chat_response=common_response.message,
            user_id=found_user.id,
            primary_lang=found_user.primary_lang,
            learning_lang=found_user.learning_lang
        )
        await update.message.reply_text(text=common_response.message)
