import os
from dotenv import load_dotenv

from polly.core import Bot

if __name__ == "__main__":
    load_dotenv()
    bot = Bot(
        {
            'TELEGRAM_TOKEN': os.getenv('TELEGRAM_TOKEN'),
            'OPENAI_TOKEN': os.getenv('OPENAI_TOKEN'),
            'OPENAI_WHISPER': os.getenv('OPENAI_WHISPER'),
            'OPENAI_GPT': os.getenv('OPENAI_GPT'),
            'GOOGLE_APPLICATION_CREDENTIALS': os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
            'DATABASE_URL': os.getenv('DATABASE_URL'),
            'REDIS_HOST': os.getenv('REDIS_HOST'),
            'REDIS_PORT': os.getenv('REDIS_PORT'),
            'REDIS_PASSWORD': os.getenv('REDIS_PASSWORD')
        }
    )
    bot.run()
