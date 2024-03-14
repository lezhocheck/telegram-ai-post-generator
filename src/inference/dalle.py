from src.inference import openai_client
from typing import Optional
import logging
from io import BytesIO
from PIL import Image
from httpx import AsyncClient
from http import HTTPStatus
from aiogram.types import BufferedInputFile


class DalleInferenceApi:
    async def generate_image(self, prompt: str, output_name: str) -> Optional[BufferedInputFile]:
        try:
            response = await openai_client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                size='1792x1024',
                quality='standard',
                n=1
            )
            return await self._compress(response.data[0].url, filename=output_name)
        except Exception as e:
            logging.error(f'Cannot generate image. Got an exception {e} with prompt {prompt}')
            return None
    
    async def _compress(self, url: str, filename: str, quality: int = 95) -> BufferedInputFile:
        async with AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != HTTPStatus.OK:
                raise ValueError('Cannot fetch image from url')
            with Image.open(BytesIO(response.content)) as img:
                output = BytesIO()
                img.convert('RGB').save(output, 'JPEG', quality=quality)
                return BufferedInputFile(output.getvalue(), filename)
