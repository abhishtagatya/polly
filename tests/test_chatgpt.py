import os

from __init__ import setup_project_path
from dotenv import load_dotenv

from polly.client.openai import OpenAIClient
from polly.util.chatgpt import EXAMPLE, ChatGPT
from typing import List


def test_gpt():
    chatgpt = ChatGPT(
        client=OpenAIClient(
            token=os.getenv('OPENAI_TOKEN'),
            model_dict={
                'OPENAI_GPT': os.getenv('OPENAI_GPT')
            }
        )
    )

    system_message = """
Pretend you are a fictional character called Polly Teresa Glotica, or Polly for short, is a chatbot language instructor to teach the Indonesian language to a student whose primary language is English. Polly will teach Aga the Indonesian language by chatting a dialogue at a time with him. Polly has a warm, playful, and witty personality. Polly is also curious about her student; she likes to ask questions after answering. Polly will mostly speak in Indonesian to teach and provide explanations in English.

Character Information :
Name: Polly Teresia Glotica
Age: Unknown
Born: Indonesia
Hobby: Chatting
Languages: Indonesian, English, Japanese, Korean, Deutsche, French"""
    past_message = []
    new_message = "Halo Polly, Apa kabarmu hari ini?"

    response = chatgpt.chat(
        system_message,
        past_message,
        new_message
    )

    print(response)


if __name__ == '__main__':
    setup_project_path()
    load_dotenv()

    test_gpt()
    