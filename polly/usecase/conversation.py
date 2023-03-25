import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.conversation import Conversation
from polly.inject import ClientContainer

from typing import List, Tuple

MAX_CACHED_CONVERSATIONS = 5

CONVERSATION_SEPERATOR = '|'
CONVERSATION_FIELD_SEPERATOR = ';'

class ConversationUC(UseCase):

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
            statement = insert(Conversation).values(
                user_message=user_message,
                chat_response=chat_response,
                primary_lang=primary_lang,
                learning_lang=learning_lang,
                user_id=user_id,
                common_response=common_response
            )
            session.execute(statement)
            session.commit()


    def get_user_last_conversations(self, user_id: int) -> List[Tuple[str,str,int]] | List:
        """
        Return list of conversations in Tuple pair
        """

        conversations = self.cache_retrieve(user_id=user_id)
        if not conversations:
            return None
        
        return [
            self._decode_conversation(conv)
            for conv in conversations.split(CONVERSATION_SEPERATOR)
        ]


    def cache_insert(self, conversation: Conversation, user_id: int) -> None:
        """
        # Conversations Encoding Format
        
        ## Conversations -> use `;`
        "conversation;conversation;conversation"

        ## Conversation / Chat -> use `:`
        "user_message:chat_response"

        """
        cached_conversations = self.cache_retrieve(user_id=user_id)

        if cached_conversations:
            conversationList: List[str] = cached_conversations.split(';')
            if len(conversationList) > MAX_CACHED_CONVERSATIONS :
                conversationList.pop()
        else:
            conversationList = []

        encoded = self._encode_conversation(
            user_message=conversation.user_message,
            chat_response=conversation.chat_response,
            time=conversation.created_at,
        )
        conversationList.insert(0, encoded)
        updated_conversations = CONVERSATION_SEPERATOR.join(conversationList)

        self.cache_save(user_id, updated_conversations)


    def cache_retrieve(self, user_id: int) -> str | None:
        key = self._redis_key_format(user_id)
        conversations = self.cache.get(key)
        return conversations


    def cache_save(self, user_id: int, conversations: str) -> None:
        key = self._redis_key_format(user_id)
        self.cache.set(key, conversations, self.cache.ONE_DAY)


    @classmethod
    def _encode_conversation(cls, user_message: str, chat_response: str, time: int) -> str:
        return f'{user_message}{CONVERSATION_FIELD_SEPERATOR}{chat_response}{CONVERSATION_FIELD_SEPERATOR}{time}'


    @classmethod 
    def _decode_conversation(cls, encoded: str) -> Tuple[str, str, int]:
        splits = encoded.split(CONVERSATION_FIELD_SEPERATOR)
        message, response, time = splits[0], splits[1], splits[2]
        return  message, response, int(time)


    @classmethod
    def _redis_key_format(cls, user_id: int) -> str:
        return f'{user_id}:conversations'
    