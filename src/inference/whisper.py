from src.inference import openai_client
from typing import Optional
import logging
from io import BytesIO
from traceback import print_exc


class WhisperInferenceApi:
    async def recognize(self, file: BytesIO) -> Optional[str]:
        try:
            transcription = await openai_client.audio.transcriptions.create(
                model='whisper-1', 
                file=file
            )
            return transcription.text
        except Exception as e:
            logging.error(f'Cannot recognize voice. Got an exception {e}.')
            print_exc()
            return None