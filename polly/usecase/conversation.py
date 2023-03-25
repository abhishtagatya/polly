import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.conversation import Conversation
from polly.inject import ClientContainer

from typing import List, Tuple, Optional


class ConversationUC(UseCase):
    N_PREV_CONVERSATION = 5

    CHAT_SEPARATOR = '|'
    CHAT_FIELD_SEPARATOR = ';'

    GET_USER_CONVERSATION = "conversations:{user_id}:{conv_id}"
    KEYS_USER_CONVERSATION = "conversations:{user_id}:*"

    def __init__(self, client: ClientContainer, logger: logging.Logger):
        super().__init__(client, logger)

    def update_conversation(self,
                            user_message: str,
                            chat_response: str,
                            primary_lang: str,
                            learning_lang: str,
                            user_id: int,
                            common_response: bool = False):
        with Session(self.db) as session:
            clean_user_msg = self.clean_conversation(user_message)
            clean_chat_msg = self.clean_conversation(chat_response)

            statement = insert(Conversation).values(
                user_message=self.clean_conversation(clean_user_msg),
                chat_response=self.clean_conversation(clean_chat_msg),
                primary_lang=primary_lang,
                learning_lang=learning_lang,
                user_id=user_id,
                common_response=common_response
            ).returning(Conversation)
            [result] = session.execute(statement).fetchone()

            if common_response is False:
                self.cache.set(
                    self.GET_USER_CONVERSATION.format(
                        user_id=user_id, conv_id=result.id
                    ),
                    self.encode_conversation(result),
                    ttl=self.cache.ONE_HOUR
                )

            session.commit()

    def get_previous_conversations(self,
                                   uid: int,
                                   primary_lang: str,
                                   learning_lang: str,
                                   limit: int = N_PREV_CONVERSATION):

        result = []
        found_keys = self.cache.keys(self.KEYS_USER_CONVERSATION.format(user_id=uid))
        selected_keys = sorted(found_keys)[-self.N_PREV_CONVERSATION:]
        for f_key in selected_keys:
            result.append(self.decode_conversation(self.cache.get(f_key)))

        if len(result) >= limit:
            return result

        with Session(self.db) as session:
            result = session.query(Conversation).filter(
                Conversation.user_id == uid,
                Conversation.primary_lang == primary_lang,
                Conversation.learning_lang == learning_lang,
                Conversation.common_response is False
            ).order_by(Conversation.created_at.desc()).limit(limit).all()

            for r in result:
                self.cache.set(
                    self.GET_USER_CONVERSATION.format(
                        user_id=uid, conv_id=r.id
                    ),
                    self.encode_conversation(r),
                    ttl=self.cache.ONE_HOUR
                )

            return reversed(result)

    @staticmethod
    def encode_conversation(conv: Conversation) -> str:
        output = ""
        output += f"{conv.user_message}{ConversationUC.CHAT_SEPARATOR}"
        output += f"{conv.chat_response}{ConversationUC.CHAT_FIELD_SEPARATOR}"
        return output

    @staticmethod
    def decode_conversation(text: str) -> Conversation:
        user_message, chat_response = text.split(ConversationUC.CHAT_SEPARATOR)
        return Conversation(
            user_message=user_message,
            chat_response=chat_response.replace(ConversationUC.CHAT_FIELD_SEPARATOR, '')
        )

    # @staticmethod
    # def encode_conversation_chain(conversations: List[Conversation]) -> str:
    #     output = ""
    #     for conv in conversations:
    #         output += ConversationUC.encode_conversation(conv)
    #     return output
    #
    # @staticmethod
    # def decode_conversation_chain(text: str) -> List[Conversation]:
    #     chain = []
    #     conversations = text.split(ConversationUC.CHAT_FIELD_SEPARATOR)
    #     for conv in conversations:
    #         chain.append(ConversationUC.decode_conversation(conv))
    #     return chain

    @staticmethod
    def format_conversation_chain(conversations: List[Conversation], name: str):
        output = ""
        for conv in conversations:
            output += f"{name}: {conv.user_message}\n"
            output += f"Polly: {conv.chat_response}\n"
        return output

    @staticmethod
    def format_conversation_tuple(conversation: List[Conversation]):
        message = []
        for conv in conversation:
            message.append(['USER', conv.user_message])
            message.append(['ASSISTANT', conv.chat_response])
        return message

    @staticmethod
    def next_conversation_chain(text: str, name: str = 'User'):
        output = ""
        output += f"{name}: {text}\n"
        output += f"Polly: "
        return output

    @staticmethod
    def clean_conversation(text: str):
        text = text.replace(ConversationUC.CHAT_SEPARATOR, '')
        text = text.replace(ConversationUC.CHAT_FIELD_SEPARATOR, '')
        return text
