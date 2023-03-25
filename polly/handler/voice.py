import logging
from io import BytesIO, FileIO

from telegram import Update
from telegram.ext import ContextTypes

from polly.handler.base import BaseHandler
from polly.usecase.user import UserUC
from polly.usecase.common_response import CommonResponseUC
from polly.usecase.conversation import ConversationUC
from polly.usecase.prompt_instruction import PromptInstructionUC
from polly.usecase.voice import VoiceUC
from polly.inject import ClientContainer


class VoiceMessageHandler(BaseHandler):

    SIZE_LIMIT = 50000

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)
        self.common_response_uc = CommonResponseUC(client, logger)
        self.user_uc = UserUC(client, logger)
        self.conversation_uc = ConversationUC(client, logger)
        self.prompt_instruct_uc = PromptInstructionUC(client, logger)
        self.voice_uc = VoiceUC(client, logger)

        self.prompt_base = self.prompt_instruct_uc.get_prompt_instruction_by_filter('POLLY_BASE')

    async def voice_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        found_user = self.user_uc.get_user_by_id(user.id)

        if found_user is None:
            common_response = self.common_response_uc.get_common_response_by_filter('UNREGISTER_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        tg_audio_file = await update.message.voice.get_file()
        if tg_audio_file.file_size > self.SIZE_LIMIT:
            common_response = self.common_response_uc.get_common_response_by_filter('VOICE_LENGTH_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        user_message = await self.voice_uc.get_voice_message(uid=user.id, file=tg_audio_file)
        past_message = self.conversation_uc.get_previous_conversations(
            uid=found_user.id, primary_lang=found_user.primary_lang, learning_lang=found_user.learning_lang
        )
        past_message_format = self.conversation_uc.format_conversation_tuple(conversation=past_message)

        chat_response = await self.voice_uc.get_chat_answer(
            past_message=past_message_format, new_message=user_message, prompt=self.prompt_base.prompt,
            instruction={
                'USER_NAME': found_user.name,
                'PRIMARY_LANG': found_user.primary_lang,
                'LEARNING_LANG': found_user.learning_lang
            }
        )

        if user_message == '':
            common_response = self.common_response_uc.get_common_response_by_filter('VOICE_PROCESS_ERROR')
            await update.message.reply_text(text=common_response.message)
            return

        voice_message_file = await self.voice_uc.create_voice_message(
            text=chat_response, lang=found_user.learning_lang, uid=found_user.id
        )

        # Update Conversation Record and Cache
        self.conversation_uc.update_conversation(
            user_message=user_message,
            chat_response=chat_response,
            user_id=found_user.id,
            primary_lang=found_user.primary_lang,
            learning_lang=found_user.learning_lang
        )

        await update.message.reply_voice(voice=voice_message_file, caption=f'Polly heard you say "{user_message}"')
