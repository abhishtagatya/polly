from typing import Dict

from polly.base import BaseBot

from polly.handler.start import StartMessageHandler
from polly.handler.change import ChangeMessageHandler
from polly.handler.text import TextMessageHandler
from polly.handler.voice import VoiceMessageHandler
from polly.handler.debug import DebugMessageHandler

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


class Bot(BaseBot):

    def __init__(self, config: Dict):
        super().__init__(config)

        start_handler = StartMessageHandler(client=self.client, logger=self.logger)
        change_handler = ChangeMessageHandler(client=self.client, logger=self.logger)
        text_handler = TextMessageHandler(client=self.client, logger=self.logger)
        voice_handler = VoiceMessageHandler(client=self.client, logger=self.logger)
        debug_handler = DebugMessageHandler(client=self.client, logger=self.logger)

        # Conversation Handler
        start_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start_handler.start_command_handler)],
            states={
                start_handler.START_ROUTES: [
                    CallbackQueryHandler(start_handler.query_explain_handler,
                                         pattern=f"^{start_handler.EXPLAIN}$"),
                    CallbackQueryHandler(start_handler.query_primary_lang_handler,
                                         pattern=f"^{start_handler.CONTINUE}$"),
                    CallbackQueryHandler(start_handler.query_learning_lang_handler,
                                         pattern=f"^.*:{start_handler.SELECTED_PRIMARY}$"),
                    CallbackQueryHandler(start_handler.end_command_handler,
                                         pattern=f"^.*:{start_handler.SELECTED_LEARNING}$"),
                ]
            },
            fallbacks=[CommandHandler("start", start_handler.start_command_handler)]
        )

        change_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("change", change_handler.change_command_handler)],
            states={
                change_handler.CHANGE_ROUTES: [
                    CallbackQueryHandler(change_handler.change_primary_lang_handler,
                                         pattern=f"^{change_handler.SELECTED_PRIMARY}$"),
                    CallbackQueryHandler(change_handler.change_learning_lang_handler,
                                         pattern=f"^{change_handler.SELECTED_LEARNING}$"),
                    CallbackQueryHandler(change_handler.end_primary_lang_handler,
                                         pattern=f"^.*:{change_handler.END_PRIMARY}$"),
                    CallbackQueryHandler(change_handler.end_learning_lang_handler,
                                         pattern=f"^.*:{change_handler.END_LEARNING}$"),
                    CallbackQueryHandler(change_handler.end_command_handler,
                                         pattern=f"^{change_handler.END}$"),
                ]
            },
            fallbacks=[CommandHandler("change", change_handler.change_command_handler)]
        )

        self.client.telegram_api.add_handler(start_conv_handler)
        self.client.telegram_api.add_handler(change_conv_handler)

        # Command Handler
        self.client.telegram_api.add_handler(CommandHandler("dconv", debug_handler.debug_conversation_handler))

        # Non-Command Handler
        self.client.telegram_api.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler.text_message_handler)
        )
        self.client.telegram_api.add_handler(
            MessageHandler(filters.VOICE, voice_handler.voice_message_handler)
        )

