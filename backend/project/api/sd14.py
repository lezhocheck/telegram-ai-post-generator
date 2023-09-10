from diffusers import StableDiffusionPipeline
from .base import BaseApi
from . import select_device
from typing import Final, Any


class SD14Api(BaseApi):
    __TITLE__: Final = 'Stable-Diffusion-v1-4'
    __DESCRIPTION__: Final = r'''Stable Diffusion is a latent 
    text-to-image diffusion model capable of 
    generating photo-realistic images given any text 
    input. The Stable-Diffusion-v1-4 checkpoint was 
    initialized with the weights of the Stable-Diffusion-v1-2 
    checkpoint and subsequently fine-tuned on 225k steps at 
    resolution 512x512 on 'laion-aesthetics v2 5+' and 
    10% dropping of the text-conditioning to improve 
    classifier-free guidance sampling.'''
    __AVAILABLE__: Final = True

    @classmethod
    def __load_model__(cls) -> Any:
        pipeline = StableDiffusionPipeline.from_pretrained(
            'CompVis/stable-diffusion-v1-4', 
            cache_dir=cls._get_path()
        ).to(select_device())
        return pipeline
    