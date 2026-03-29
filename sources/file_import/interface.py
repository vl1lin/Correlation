from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path


class FileStrategy(ABC):
    """Стратегия чтения файлов"""
    @abstractmethod
    def file_read(self, *, file_path: Union[Path, str]) -> Any:
        pass
