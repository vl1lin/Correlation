import logging
from typing import Any
from interface import FileStrategy
import csv
from pathlib import Path


logger = logging.getLogger(__name__)


class CsvStrategy(FileStrategy):
    def _file_read(self, *, file_path: str) -> Any:
        path = Path(file_path)

        logger.info(f"Проверка существования файла: {file_path}")
        if not path.exists():
            logger.error(f"Файл {file_path} не найден")
            raise FileNotFoundError(f"Файл {file_path} не найден")

        logger.info(f"Чтение файла: {file_path}")
        with open(file_path, "r", encoding='utf-8') as f:
            try:
                data = csv.reader(f)
                logger.info(f"Чтение файла: {file_path} успешно завершено")
            except csv.Error as e:
                logger.error(f"Ошибка в формате csv файла: {e}")
                raise ValueError(f"Ошибка {e}")
        return data
