from io import FileIO

SUPPORTED_WHISPER_FILETYPE = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

def load_audio(filepath: str) -> FileIO:
    file_extenstion = filepath.split('.')[-1]
    if not file_extenstion in SUPPORTED_WHISPER_FILETYPE:
        raise Exception(f'Unsupported file type : {file_extenstion}')

    file = FileIO(filepath, 'r')
    return file