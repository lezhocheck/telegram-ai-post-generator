from typing import Any


class StateManager:
    __STATES__: dict[str, Any] = dict()

    @classmethod
    def __getattr__(cls, name: str) -> Any:
        if name not in cls.__STATES__:
            raise KeyError(f'State {name} not found in state manager')
        return cls.__STATES__[name]
    
    @classmethod
    def __setattr__(cls, name: str, value: Any) -> None:
        cls.__STATES__[name] = value

    @classmethod
    def clear(cls) -> None:
        cls.__STATES__.clear()