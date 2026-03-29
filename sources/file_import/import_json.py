import logging
from interface import FileStrategy
from typing import Any
from pathlib import Path
import json


logger = logging.getLogger(__name__)


class JsonStrategy(FileStrategy):
    def _file_read(self, *, file_path: str) -> Any:
        path = Path(file_path)

        logger.info(f"Проверка существования файла")
        if not path.exists():
            logger.error(f"Файл: {file_path} не найден")
            raise FileNotFoundError(f"Файл: {file_path} не найден")

        logger.info(f"Загрузка данных: {file_path}")
        with open(file_path, "r", encoding='utf-8') as f:
            try:
                data = json.load(f)
                logger.info(f"Данные успешно загружены в формате: {type(data)}")
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка формата JSON: {e}")
                raise ValueError(f"Ошибка формата JSON: {e}")
        return data
