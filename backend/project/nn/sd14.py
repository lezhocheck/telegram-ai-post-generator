from diffusers import StableDiffusionPipeline
import os
from . import get_device
from project.models import Model
from flask import Flask, current_app
import functools


class SD14Api:
    TITLE = 'Stable-Diffusion-v1-4'
    DESCRIPTION = f'''Stable Diffusion is a latent 
    text-to-image diffusion model capable of 
    generating photo-realistic images given any text 
    input. The Stable-Diffusion-v1-4 checkpoint was 
    initialized with the weights of the Stable-Diffusion-v1-2 
    checkpoint and subsequently fine-tuned on 225k steps at 
    resolution 512x512 on 'laion-aesthetics v2 5+' and 
    10% dropping of the text-conditioning to improve 
    classifier-free guidance sampling.'''
    AVAILABLE = True

    @staticmethod
    def build_model() -> Model:
        return Model(title=SD14Api.TITLE, description=SD14Api.DESCRIPTION, available=SD14Api.AVAILABLE)

    @staticmethod
    def _get_path() -> os.path:
        return os.path.join(current_app.config['STATIC_FOLDER'], SD14Api.TITLE)

    @functools.lru_cache(maxsize=None)
    @staticmethod
    def load_api() -> None:
        pipeline = StableDiffusionPipeline.from_pretrained(
            'CompVis/stable-diffusion-v1-4', 
            cache_dir=SD14Api._get_path()
        ).to(get_device())
        return pipeline
    
    @staticmethod
    def run(prompt: str, path: os.path) -> None:
        api = SD14Api.load_api()
        image = api(prompt=prompt).images[0]
        image.save(path)
    