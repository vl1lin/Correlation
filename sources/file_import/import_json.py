import logging
from interface import FileStrategy
from typing import Any, Union
from pathlib import Path


logger = logging.getLogger(__name__)


class JsonStrategy(FileStrategy):
    def file_read(self, *, file_path: Union[Path, str]) -> Any:
        logger.info(f"Загрузка данных: {file_path}")

