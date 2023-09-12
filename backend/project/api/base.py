from abc import ABCMeta
from typing import Callable, Any
from project.models.model import Model
import os
from flask import current_app


class BaseApi(metaclass=ABCMeta):    
    @classmethod
    def _get_path(cls) -> str:
        title: str = getattr(cls, '__TITLE__')
        with current_app.app_context():
            return os.path.join(current_app.config['STATIC_FOLDER'], title) 
    
    @classmethod
    def preload(cls) -> Model:
        load_model: Callable[[], Any] = getattr(cls, '__load_model__')
        load_model()
        return Model(title=getattr(cls, '__TITLE__'), 
                     description=getattr(cls, '__DESCRIPTION__'), 
                     available=getattr(cls, '__AVAILABLE__'))
    
    @classmethod
    def run(cls, prompt: str, path: str) -> None:
        load_model: Callable[[], Any] = getattr(cls, '__load_model__')
        api = load_model()
        images = api(prompt).images
        print(f'{len(images)} generated')
        images[0].save(path)