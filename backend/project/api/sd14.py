from diffusers import StableDiffusionPipeline
from .base import BaseApi
from . import select_device
from typing import Final, Any
from project.models.model import Model, Type


class SD14Api(BaseApi):
    __MODEL__ = Model(
        title='Stable-Diffusion-v1-4',
        content_type=Type.IMAGE_PNG,
        description=r'Stable Diffusion is a latent' 
            r'text-to-image diffusion model capable of' 
            r'generating photo-realistic images given any text' 
            r'input. The Stable-Diffusion-v1-4 checkpoint was' 
            r'initialized with the weights of the Stable-Diffusion-v1-2' 
            r'checkpoint and subsequently fine-tuned on 225k steps at' 
            r'resolution 512x512 on "laion-aesthetics v2 5+" and' 
            r'10% dropping of the text-conditioning to improve' 
            r'classifier-free guidance sampling.',
        is_available=False
    )

    @classmethod
    def __load_model__(cls) -> Any:
        model_id: Final[str] = 'CompVis/stable-diffusion-v1-4'
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            cache_dir=cls._get_path()
        ).to(select_device())
        return pipeline
    