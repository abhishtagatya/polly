import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from polly.handler.base import BaseHandler
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.user import UserUC
from polly.util.telegram import split_inline_keyboard
from polly.const import ConversationState, LANGUAGE_OPTION
from polly.inject import ClientContainer


class StartMessageHandler(BaseHandler):

    START_ROUTES = ConversationState.START_ROUTE

    CONTINUE = 0
    EXPLAIN = 1
    SELECTED_PRIMARY = 2
    SELECTED_LEARNING = 3
    END = 4

    EXPLAIN_URL = "https://lablab.ai/event/chatgpt-api-and-whisper-api-global-hackathon/magnalingua/pollyglotica"

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)

    async def start_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send message on `/start`."""

        user = update.message.from_user
        self.logger.info(f"{user} started the conversation.")

        keyboard = [[
            InlineKeyboardButton("Continue", callback_data=self.CONTINUE),
            InlineKeyboardButton("Explain", callback_data=self.EXPLAIN)
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        common_response = self.common_response_uc.get_common_response_by_filter('GREET_START')
        await update.message.reply_text(common_response.message, reply_markup=reply_markup)

        return self.START_ROUTES

    async def query_explain_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query to explain """

        query = update.callback_query
        await query.answer()

        keyboard = [[
            InlineKeyboardButton("Website", url=self.EXPLAIN_URL),
            InlineKeyboardButton("Continue", callback_data=self.CONTINUE)
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        common_response = self.common_response_uc.get_common_response_by_filter('EXPLAIN_START')
        await query.edit_message_text(text=common_response.message, reply_markup=reply_markup)

        return self.START_ROUTES

    async def query_primary_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query after select continue"""

        query = update.callback_query
        await query.answer()

        keyboard = [
            InlineKeyboardButton(
                name, callback_data=f"{code}:{self.SELECTED_PRIMARY}"
            ) for (code, name) in LANGUAGE_OPTION.items()
        ]
        reply_markup = InlineKeyboardMarkup(split_inline_keyboard(keyboard))
        common_response = self.common_response_uc.get_common_response_by_filter('PRIMARY_START')
        await query.edit_message_text(text=common_response.message, reply_markup=reply_markup)

        return self.START_ROUTES

    async def query_learning_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query after select primary language"""

        query = update.callback_query
        await query.answer()

        user_data = context.user_data
        user_data['primary_lang'] = query.data.split(":")[0]

        new_lang_option = dict(LANGUAGE_OPTION)
        new_lang_option.pop(user_data['primary_lang'])

        keyboard = [
            InlineKeyboardButton(
                name, callback_data=f"{code}:{self.SELECTED_LEARNING}"
            ) for (code, name) in new_lang_option.items()
        ]
        reply_markup = InlineKeyboardMarkup(split_inline_keyboard(keyboard))
        common_response = self.common_response_uc.get_common_response_by_filter('LEARNING_START')
        await query.edit_message_text(text=common_response.message.format(
            primary_lang=LANGUAGE_OPTION[user_data['primary_lang']]
        ), reply_markup=reply_markup)

        return self.START_ROUTES

    async def end_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback end query after select target language"""

        query = update.callback_query
        user = query.from_user
        await query.answer()

        user_data = context.user_data
        user_data['learning_lang'] = query.data.split(":")[0]

        self.user_uc.create_or_update_user(
            uid=user.id,
            name=user.first_name,
            username=user.username,
            messaging_lang=user.language_code.upper(),
            primary_lang=user_data['primary_lang'],
            learning_lang=user_data['learning_lang'],
        )

        common_response = self.common_response_uc.get_common_response_by_filter('END_START')
        await query.edit_message_text(text=common_response.message.format(
            learning_lang=LANGUAGE_OPTION[user_data['learning_lang']],
            primary_lang=LANGUAGE_OPTION[user_data['primary_lang']]
        ))

        return ConversationHandler.END
