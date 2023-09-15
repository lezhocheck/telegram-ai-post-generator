from abc import ABCMeta
from typing import Callable, Any, Iterator
from project.models.model import Model
from project.models.content import Content
from project.models.query import Query
import os
from flask import current_app, url_for
from uuid import uuid4
from datetime import datetime
from typing import Type


class BaseApi(metaclass=ABCMeta):    
    @classmethod
    def _model(cls) -> Model:
        return getattr(cls, '__MODEL__')

    @classmethod
    def _get_path(cls) -> str:
        model: Model = cls._model()
        with current_app.app_context():
            return os.path.join(current_app.config['STATIC_FOLDER'], model.title) 

    @classmethod
    def _load_api(cls) -> Any:
        if not cls._model().is_available:
            raise ValueError('Model is not available')
        load_model: Callable[[], Any] = getattr(cls, '__load_model__')
        return load_model()

    @classmethod
    def preload(cls) -> Model:
        cls._load_api()
        return cls._model()
    
    @staticmethod
    def from_model(model: Model) -> Type['BaseApi']:
        subclasses: list[Type[BaseApi]] = BaseApi.__subclasses__()
        for subcls in subclasses:      
            title = subcls._model().title
            if title == model.title:
                return subcls
        raise ValueError(f'No API found for model {model}')

    @classmethod
    def run(cls, query: Query) -> Iterator[Content]:
        api = cls._load_api()
        content_folder = current_app.config['CONTENT_FOLDER']
        output = api(query.prompt)
        for image in output.images:
            uuid = uuid4().hex
            local_path = os.path.join(
                content_folder, 
                f'{uuid}.{cls._model().content_type}'
            )
            public_url = url_for(
                'Static.StaticContent', 
                filename=uuid, _external=True
            )
            print(image)
            print(type(image))
            image.save(local_path)
            yield Content(
                query_id=query.id, 
                link_to_disk=public_url,
                generated_at=datetime.utcnow()
            )