import json
import numpy as np
import pandas as pd
import random
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, Union, Callable
from pathlib import Path


class FileStrategy(ABC):
    @abstractmethod
    def read(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        pass

    @abstractmethod
    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[Path, str]) -> None:
        pass


class JsonStrategy(FileStrategy):
    def read(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return pd.json_normalize(data)
        else:
            return pd.DataFrame([data])

    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[Path, str]) -> None:
        data.to_json(file_path_to_write, orient="records", force_ascii=False)


class CsvStrategy(FileStrategy):
    def read(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        return pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")

    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[Path, str]) -> None:
        data.to_csv(file_path_to_write, index=False, encoding="utf-8")


class TxtStrategy(FileStrategy):
    def __init__(self, *, delimetr: str = '\\t'):
        self.delimiter = delimetr

    def read(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        return pd.read_csv(file_path, sep=self.delimiter, header=None, names=["col_1", "col_2"])

    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[Path, str]) -> None:
        data.to_csv(file_path_to_write, sep=self.delimiter, index=False, header=False)


class DataProcessor:
    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._strategies: Dict[str, FileStrategy] = {
            "csv": CsvStrategy(),
            "json": JsonStrategy(),
            "txt": TxtStrategy()
        }

    def _get_strategy(self, *, file_path: Union[str, Path]) -> FileStrategy:
        ext = file_path.split('.')[-1].lower()
        if ext not in self._strategies:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")
        return self._strategies[ext]

    def load_file(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        strategy = self._get_strategy(file_path=file_path)
        self._data = strategy.read(file_path=file_path)
        print(f"Данные успешно загружены из {file_path} в {self._data}")
        return self._data

    def transform_data(self, *, func: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        if self._data is None:
            raise ValueError("Сначала загрузите данные")
        else:
            self._data = func(self._data)
