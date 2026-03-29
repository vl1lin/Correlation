import random
from dataclasses import dataclass
from typing import Optional
import logging


logger = logging.getLogger(__name__)


@dataclass
class RandomConfig:
    seed: Optional[int] = 42
    use_numpy: bool = False


class RandomGenerator:
    def __init__(self, config: RandomConfig):
        self.config = config
        self._seed = config.seed
        random.seed(self._seed)

    @classmethod
    def with_seed(cls, seed: Optional[int]):
        config = RandomConfig(seed=seed)
        return cls(config)

