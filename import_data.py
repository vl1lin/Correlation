import json
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
    def __init__(self, *, delimiter: str = '\t'):
        self.delimiter = delimiter

    def read(self, *, file_path: Union[str, Path]) -> pd.DataFrame:
        return pd.read_csv(file_path, sep=self.delimiter, header=None, names=["col_1", "col_2"])

    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[str, Path]) -> None:
        data.to_csv(file_path_to_write, sep=self.delimiter, index=False, header=False)


class DataProcessor:
    def __init__(self, *, base_dir: Optional[Path] = None):
        self._data: Optional[pd.DataFrame] = None
        self._base_dir = base_dir or Path(__file__).resolve().parent / "data"

        self._strategies: Dict[str, FileStrategy] = {
            "csv": CsvStrategy(),
            "json": JsonStrategy(),
            "txt": TxtStrategy()
        }

    def _get_file_path(self, *, file_name: Union[str, Path]) -> Path:
        path = Path(file_name)

        # Если указан полный путь
        if path.is_absolute() and path.exists():
            return path

        # Поиск в текущей директории
        if path.exists():
            return path

        # Поиск в папке data/
        alt_path = self._base_dir / path
        if alt_path.exists():
            return alt_path

        raise FileNotFoundError(
            f"Файл не найден: '{file_name}'. "
            f"Проверено в текущей директории и '{self._base_dir}'"
        )

    def _get_strategy(self, *, file_path: Union[str, Path]) -> FileStrategy:
        path = Path(file_path)
        ext = path.suffix.lstrip('.').lower()
        if ext not in self._strategies:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")
        return self._strategies[ext]

    def load_file(self, *, file_name: Union[str, Path]) -> pd.DataFrame:
        full_path = self._get_file_path(file_name=file_name)
        strategy = self._get_strategy(file_path=full_path)
        self._data = strategy.read(file_path=full_path)
        print(f"Данные успешно загружены из {full_path}")
        return self._data

    def get_column(self, *, column_name: str) -> list:
        if self._data is None:
            raise ValueError("Сначала загрузите данные")
        return self._data[column_name].tolist()

    def get_values(self) -> list:
        if self._data is None:
            raise ValueError("Сначала загрузите данные")
        if 'values' in self._data.columns:
            return self._data['values'].tolist()
        elif 'value' in self._data.columns:
            return self._data['value'].tolist()
        else:
            return self._data.iloc[:, 0].tolist()

    def get_bounds(self) -> tuple:
        if self._data is None:
            raise ValueError("Сначала загрузите данные")

            # Если self._data — DataFrame
        if hasattr(self._data, 'iloc'):
            lower = float(str(self._data['lower_bound'].iloc[0]).replace(',', '.'))
            upper = float(str(self._data['upper_bound'].iloc[0]).replace(',', '.'))
        else:
            lower = float(str(self._data.get('lower_bound')).replace(',', '.'))
            upper = float(str(self._data.get('upper_bound')).replace(',', '.'))

        return lower, upper

    def transform_data(self, *, func: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        if self._data is None:
            raise ValueError("Сначала загрузите данные")
        self._data = func(self._data)

    def save_file(self, *, file_path: Union[str, Path]) -> None:
        if self._data is None:
            raise ValueError("Нет данных для сохранения")
        strategy = self._get_strategy(file_path=file_path)
        strategy.write(data=self._data, file_path_to_write=file_path)
        print(f"Данные сохранены в файл {file_path}")

    @property
    def data(self) -> Optional[pd.DataFrame]:
        return self._data
