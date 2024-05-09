from typing import final
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel


@final
class Prompts(BaseModel):
    gpt_post_text_path: str = './src/inference/prompts/gpt-post-text.txt'
    gpt_image_required_path: str = './src/inference/prompts/gpt-image-required.txt'


@final
class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    db: PostgresDsn
    service_host: str
    bot_token: str
    telegram_secret: str

    openai_key: str
    test_mode: bool

    gpt_inference_model: str = 'gpt-3.5-turbo-0125'
    prompts: Prompts = Prompts()


ENV = Env()