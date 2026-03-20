from models.Standing import Standing
from core import Correlation


class CorrelationFactory:
    _registry = {
        "standing": Standing
    }

    @classmethod
    def create(cls, *, name: str, **kwargs) -> Correlation:
        if name not in cls._registry:
            raise ValueError(f"Неизвестная корреляция {name}")
        return cls._registry[name](**kwargs)
