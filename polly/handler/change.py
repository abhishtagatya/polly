import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from polly.handler.base import BaseHandler
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.user import UserUC
from polly.util.telegram import split_inline_keyboard
from polly.const import ConversationState, LANGUAGE_OPTION
from polly.inject import ClientContainer


class ChangeMessageHandler(BaseHandler):

    CHANGE_ROUTES = ConversationState.CHANGE_ROUTE

    SELECTED_PRIMARY = 0
    SELECTED_LEARNING = 1
    END_PRIMARY = 2
    END_LEARNING = 3
    END = 4

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)

    async def change_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Send message on /change """

        user = update.message.from_user

        keyboard = [
            InlineKeyboardButton(text="Primary Language", callback_data=self.SELECTED_PRIMARY),
            InlineKeyboardButton(text="Learn Others", callback_data=self.SELECTED_LEARNING),
            InlineKeyboardButton(text="Cancel", callback_data=self.END)
        ]
        reply_markup = InlineKeyboardMarkup(split_inline_keyboard(keyboard, split=1))
        common_response = self.common_response_uc.get_common_response_by_filter('GREET_CHANGE')
        await update.message.reply_text(common_response.message, reply_markup=reply_markup)

        return self.CHANGE_ROUTES

    async def change_primary_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query after select primary lang"""

        query = update.callback_query
        await query.answer()

        keyboard = [
            InlineKeyboardButton(
                name, callback_data=f"{code}:{self.END_PRIMARY}"
            ) for (code, name) in LANGUAGE_OPTION.items()
        ] + [InlineKeyboardButton(text="Cancel", callback_data=self.END)]
        reply_markup = InlineKeyboardMarkup(split_inline_keyboard(keyboard))
        common_response = self.common_response_uc.get_common_response_by_filter('PRIMARY_CHANGE')
        await query.edit_message_text(text=common_response.message, reply_markup=reply_markup)

        return self.CHANGE_ROUTES

    async def change_learning_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query after select learning lang"""

        query = update.callback_query
        await query.answer()

        keyboard = [
            InlineKeyboardButton(
                name, callback_data=f"{code}:{self.END_LEARNING}"
            ) for (code, name) in LANGUAGE_OPTION.items()
        ] + [InlineKeyboardButton(text="Cancel", callback_data=self.END)]
        reply_markup = InlineKeyboardMarkup(split_inline_keyboard(keyboard))
        common_response = self.common_response_uc.get_common_response_by_filter('LEARNING_CHANGE')
        await query.edit_message_text(text=common_response.message, reply_markup=reply_markup)

        return self.CHANGE_ROUTES

    async def end_primary_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback end query after change primary language"""

        query = update.callback_query
        await query.answer()

        user_data = context.user_data
        user_data['primary_lang'] = query.data.split(":")[0]

        user = query.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        self.user_uc.create_or_update_user(
            uid=found_user.id,
            name=found_user.name,
            username=user.username,
            messaging_lang=user.language_code.upper(),
            primary_lang=user_data['primary_lang'],
            learning_lang=found_user.learning_lang
        )

        common_response = self.common_response_uc.get_common_response_by_filter('END_CHANGE')
        await query.edit_message_text(text=common_response.message.format(
            learning_lang=LANGUAGE_OPTION[found_user.learning_lang],
            primary_lang=LANGUAGE_OPTION[user_data['primary_lang']]
        ))

        return ConversationHandler.END

    async def end_learning_lang_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback end query after change learning language"""

        query = update.callback_query
        await query.answer()

        user_data = context.user_data
        user_data['learning_lang'] = query.data.split(":")[0]

        user = query.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        self.user_uc.create_or_update_user(
            uid=found_user.id,
            name=found_user.name,
            username=user.username,
            messaging_lang=user.language_code.upper(),
            primary_lang=found_user.primary_lang,
            learning_lang=user_data['learning_lang']
        )

        common_response = self.common_response_uc.get_common_response_by_filter('END_CHANGE')
        await query.edit_message_text(text=common_response.message.format(
            learning_lang=LANGUAGE_OPTION[user_data['learning_lang']],
            primary_lang=LANGUAGE_OPTION[found_user.primary_lang]
        ))

        return ConversationHandler.END

    async def end_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query to end action """

        query = update.callback_query
        await query.answer()

        common_response = self.common_response_uc.get_common_response_by_filter('CANCEL_CHANGE')
        await query.edit_message_text(text=common_response.message)

        return ConversationHandler.END
