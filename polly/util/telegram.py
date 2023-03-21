from typing import List, Any


def split_inline_keyboard(buttons: List[Any], split: int = 2):
    return [buttons[i:i + split] for i in range(0, len(buttons), split)]
