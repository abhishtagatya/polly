from __init__ import setup_project_path
from dotenv import load_dotenv
setup_project_path()
load_dotenv()

from polly.client.openai import OpenAIClient
from polly.util.chatgpt import Massage, ChatGpt
from typing import List

def show_massages(massages: List[Massage]) -> None:
    for massage in massages:
        print(f'[{massage.role}]: {massage.text}')

def test_gpt(api_key: str):
    instruction = """
        Partner is the the bot that like to do a conversation with the user with enthusiast and friendly.
        At the first conversation, it ask which topic that user like to talk about and discuss about it later on.
        It does not like discuss anything political or sexual.
        As a godd bot, it should ask for more time to chat after user close the conversation.
    """
    client = OpenAIClient(token=api_key)
    chatgpt = ChatGpt(client=client.openai_api, temperature=1)
    """
    Temperature behaviour
    Temp: .3    The bot is not interesting. May repeat the same question. 
    Temp:  1    The bot is really good at being interesting.
                It likes to elaborate more about our prompt and response with more verbose question. 
    """
    
    bot_name = 'partner'
    username = 'user'
    conversations = [
        Massage(bot_name, "Hello!, I'm your conversation partner, what topic would you like talk about?")
    ]

    last_input = '<>'
    while last_input:
        bot_prompt = conversations[-1]
        print(f'{bot_prompt.role}: {bot_prompt.text}')
        user_input = input(f'{username}: ')

        if user_input.lower() in ['bye', 'exit']:
            break
    
        # Need to clean user input?
        user_prompt = Massage(username, user_input)
        conversations.append(user_prompt)
        
        last_five_massages = conversations[-5:]
        bot_response = chatgpt.complete(instruction, last_five_massages, bot_name)
        conversations.append(Massage(bot_name, bot_response))
        

if __name__ == '__main__':
    import os
    test_gpt(os.environ.get('OPENAI_TOKEN'))
