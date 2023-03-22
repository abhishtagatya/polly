import openai
from typing import List
from dataclasses import dataclass

@dataclass
class Massage:
    role: str
    text: str

class ChatGpt:
    def __init__(
            self,
            client: openai,
            model='text-davinci-003',
            temperature=1,
            max_tokens=120
        ):
        """
        Available params can be seen in https://platform.openai.com/docs/api-reference/completions/create 
        """
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def complete(self, instruction: str, conversations: List[Massage], bot_name='bot') -> str:
        prompt = instruction + '\n\n'

        # Fill the conversations 
        for massage in conversations:
            chat_prompt = f'{massage.role}: {massage.text}\n'
            prompt += chat_prompt
        
        prompt += bot_name

        response = self.client.Completion.create(
            model=self.model,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response['choices'][0]['text']
    