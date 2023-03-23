import asyncio
import os

from __init__ import setup_project_path
from dotenv import load_dotenv

setup_project_path()
load_dotenv()

from polly.client.gcloud import GoogleCloudClient
from polly.util.google_tts import GoogleTTS


def test_gtts():
    prompt = "こんにちわみんなさん、元気ですか？"
    gcloud_client = GoogleCloudClient(credential_file='google-credentials.json')
    tts = GoogleTTS(client=gcloud_client)
    tts.synthesize(text=prompt, lang='JP')


if __name__ == '__main__':
    test_gtts()
