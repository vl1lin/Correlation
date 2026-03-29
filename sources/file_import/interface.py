from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
import logging


logger = logging.getLogger(__name__)


class FileStrategy(ABC):
    """Стратегия чтения файлов"""
    @abstractmethod
    def _file_read(self, *, file_path: str) -> Any:
        pass

    def create_storage(self, *, file_path: str) -> pd.DataFrame:
        logger.info(f"Получение данных методом _file_read")
        data = self._file_read(file_path=file_path)

        logger.info(f"Конвертация данных в DataFrame")
        if isinstance(data, list):
            return pd.json_normalize(data)
        else:
            return pd.DataFrame(data)
