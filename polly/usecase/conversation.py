import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from polly.usecase.base import UseCase
from polly.model.conversation import Conversation
from polly.inject import ClientContainer

from typing import List, Tuple

MAX_CACHED_CONVERSATIONS = 5


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


    def get_user_last_conversations(self, user_id: int) -> List[Tuple[str,str]] | List:
        """
        Return list of conversations in Tuple pair
        """

        conversations = self.cache_retrieve(user_id=user_id)
        if not conversations:
            return None
        return conversations.split(';')


    def cache_insert(self, conversation: Conversation, user_id: int) -> None:
        """
        # Conversations Encoding Format
        
        ## Conversations -> use `;`
        "conversation;conversation;conversation"

        ## Conversation / Chat -> use `:`
        "user_message:chat_response"
        """
        encoded = self._encode_conversation(conversation)
        cached_conversations = self.cache_retrieve(user_id=user_id)

        if cached_conversations:
            conversationList: List[str] = cached_conversations.split(';')
            if len(conversationList) > MAX_CACHED_CONVERSATIONS :
                conversationList.pop()
        else:
            conversationList = []

        conversationList.insert(0, encoded)
        updated_conversations = ';'.join(conversationList)

        self.cache_save(user_id, updated_conversations)


    def cache_retrieve(self, user_id: int) -> str | None:
        key = self._redis_key_format(user_id)
        conversations = self.cache.get(key)
        return conversations


    def cache_save(self, user_id: int, conversations: str) -> None:
        key = self._redis_key_format(user_id)
        self.cache.set(key, conversations, self.cache.ONE_DAY)


    @classmethod
    def _encode_conversation(user_message: str, chat_response: str) -> str:
        return f'{user_message}:{chat_response}'


    @classmethod 
    def _decode_conversation(encoded: str) -> Tuple[str, str]:
        splits = encoded.split(':')
        return splits[0], splits[1]


    @classmethod
    def _redis_key_format(user_id: int) -> str:
        return f'{user_id}:conversations'
    