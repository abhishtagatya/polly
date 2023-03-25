import logging

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.conversation import ConversationUC
from polly.usecase.prompt_instruction import PromptInstructionUC
from polly.usecase.text import TextUC
from polly.inject import ClientContainer


class TextMessageHandler(BaseHandler):

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)
        self.conversation_uc = ConversationUC(client, logger)
        self.prompt_instruct_uc = PromptInstructionUC(client, logger)
        self.text_uc = TextUC(client, logger)

        self.prompt_base = self.prompt_instruct_uc.get_prompt_instruction_by_filter('POLLY_BASE')

    async def text_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Send message on any text message """

        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        past_message = self.conversation_uc.get_previous_conversations(
            uid=found_user.id, primary_lang=found_user.primary_lang, learning_lang=found_user.learning_lang
        )
        past_message_format = self.conversation_uc.format_conversation_tuple(conversation=past_message)
        new_message = update.message.text

        chat_response = await self.text_uc.get_chat_answer(
            past_message=past_message_format, new_message=new_message, prompt=self.prompt_base.prompt,
            instruction={
                'USER_NAME': found_user.name,
                'PRIMARY_LANG': found_user.primary_lang,
                'LEARNING_LANG': found_user.learning_lang
            }
        )

        # Update Conversation Record and Cache
        self.conversation_uc.update_conversation(
            user_message=new_message,
            chat_response=chat_response,
            user_id=found_user.id,
            primary_lang=found_user.primary_lang,
            learning_lang=found_user.learning_lang
        )
        await update.message.reply_text(text=chat_response)
