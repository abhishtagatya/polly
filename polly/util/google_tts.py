import os

from google.cloud.texttospeech_v1 import (
    TextToSpeechClient,
    SynthesisInput,
    AudioConfig,
    AudioEncoding,
    VoiceSelectionParams,
    SsmlVoiceGender
)
from google.oauth2 import service_account

from polly.client.gcloud import GoogleCloudClient


class GoogleTTS:
    SUPPORTED_LANGUAGES = {
        'ID': {'code': 'id-ID', 'name': 'id-ID-Standard-A'},
        'EN': {'code': 'en-GB', 'name': 'en-GB-Standard-A'},
        'JP': {'code': 'ja-JP', 'name': 'ja-JP-Standard-B'},
        'KO': {'code': 'ko-KR', 'name': 'ko-KR-Standard-A'},
        'DE': {'code': 'de-DE', 'name': 'de-DE-Standard-C'},
        'FR': {'code': 'fr-FR', 'name': 'fr-FR-Standard-C'}
    }

    def __init__(self, client: GoogleCloudClient):
        self.tts_client = TextToSpeechClient(credentials=client.credentials)

    def synthesize(self, text: str, lang: str, out_file: str = 'temp/temp.ogg',
                   enc: AudioEncoding = AudioEncoding.OGG_OPUS):
        synth_input = SynthesisInput({'text': text})
        audio_config = AudioConfig({
            'audio_encoding': enc
        })
        voice_profile = VoiceSelectionParams({
            'language_code': self.SUPPORTED_LANGUAGES[lang]['code'],
            'name': self.SUPPORTED_LANGUAGES[lang]['name'],
            'ssml_gender': SsmlVoiceGender.FEMALE
        })

        response = self.tts_client.synthesize_speech(
            input=synth_input, audio_config=audio_config, voice=voice_profile
        )

        with open(out_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
