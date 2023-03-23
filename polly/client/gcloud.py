import os.path

from google.oauth2 import service_account


class GoogleCloudClient:

    def __init__(self, credential_file: str):
        if not os.path.exists(credential_file):
            raise FileNotFoundError(f'Google Cloud Service Account Key under `{credential_file}` is not found.')

        self.credentials = service_account.Credentials.from_service_account_file(credential_file)
