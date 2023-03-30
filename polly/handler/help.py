import logging

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.const import LANGUAGE_OPTION
from polly.inject import ClientContainer


class HelpMessageHandler(BaseHandler):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)

    async def help_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Sends help message """

        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        help_response = self.common_response_uc.get_common_response_by_filter('BOT_HELP')
        await update.message.reply_text(text=help_response.message.format(
            learning_lang=LANGUAGE_OPTION[found_user.learning_lang]
        ))
