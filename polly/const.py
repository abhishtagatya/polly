from enum import Enum

LANGUAGE_OPTION = {
    'ID': 'Indonesian',
    'EN': 'English',
    'JP': 'Japanese',
    'KO': 'Korean',
    'DE': 'German',
    'FR': 'French'
}


class ConversationState(Enum):
    START_ROUTE = 0
    CHANGE_ROUTE = 1
    END_ROUTES = 2
