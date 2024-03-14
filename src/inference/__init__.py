from openai import AsyncOpenAI
from src.env import ENV


openai_client = AsyncOpenAI(api_key=ENV.openai_key)