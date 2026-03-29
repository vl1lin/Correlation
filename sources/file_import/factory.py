from import_json import JsonStrategy
from import_csv import CsvStrategy
import logging


logger = logging.getLogger(__name__)


class FileImportFactory:
    _registry = {
        "json": JsonStrategy,
        "csv": CsvStrategy
    }

    @classmethod
    def create_file_import_strategy(cls, *, name: str, **kwargs):
        logger.info(f"Проверка наличия стратегии")
        if name not in cls._registry:
            logger.error(f"Передана несуществующая стратегия {name}")
            raise ValueError(f"Передана несуществующая стратегия {name}")
        return cls._registry[name](**kwargs)
