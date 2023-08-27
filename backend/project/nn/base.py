from abc import ABCMeta, abstractmethod
import os
import torch
from project.models import Model


class BaseGeneratorApi(metaclass=ABCMeta):
    def __init__(self) -> None:
        if not hasattr(self, 'TITLE'):
            raise ValueError('TITLE attribute must be specified')
        if not hasattr(self, 'DESCRIPTION'):
            raise ValueError('DESCRIPTION attribute must be specified')
        if not hasattr(self, 'AVAILABLE'):
            raise ValueError('AVAILABLE attribute must be specified')

    @property
    def model(self) -> Model:
        return Model(title=self.TITLE, description=self.DESCRIPTION, available=self.AVAILABLE)

    @abstractmethod
    def preload(self, device: torch.device) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def run(self, prompt: str, path: os.path) -> None:
        raise NotImplementedError()