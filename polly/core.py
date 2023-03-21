from .base import BaseEngine

from .handler.start import StartMessageHandler
from .handler.text import TextMessageHandler
from .handler.voice import VoiceMessageHandler

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


class Bot(BaseEngine):

    def __init__(self, telegram_token: str, openai_token: str, database_uri: str, redis_cred: tuple):
        super().__init__(telegram_token, openai_token, database_uri, redis_cred)

        start_handler = StartMessageHandler(openai_api=self.openapi_api, db=self.db, cache=self.redis, logger=self.logger)
        text_handler = TextMessageHandler(openai_api=self.openapi_api, db=self.db, cache=self.redis, logger=self.logger)
        voice_handler = VoiceMessageHandler(openai_api=self.openapi_api, db=self.db, cache=self.redis, logger=self.logger)

        # Conversation Handler
        start_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start_handler.start_command_handler)],
            states={
                start_handler.START_ROUTE: [
                    CallbackQueryHandler(start_handler.query_explain_handler, pattern=f"^{start_handler.EXPLAIN}$"),
                    CallbackQueryHandler(start_handler.query_primary_lang_handler, pattern=f"^{start_handler.CONTINUE}$"),
                    CallbackQueryHandler(start_handler.query_learning_lang_handler,
                                         pattern=f"^.*:{start_handler.SELECTED_PRIMARY}$"),
                    CallbackQueryHandler(start_handler.end_command_handler,
                                         pattern=f"^.*:{start_handler.SELECTED_LEARNING}$"),
                ]
            },
            fallbacks=[CommandHandler("start", start_handler.start_command_handler)]
        )
        self.telegram_api.add_handler(start_conv_handler)

        # Command Handler

        # Non-Command Handler
        self.telegram_api.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler.text_message_handler))
        self.telegram_api.add_handler(MessageHandler(filters.VOICE, voice_handler.voice_message_handler))

