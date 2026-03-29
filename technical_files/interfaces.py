from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class DataSources(ABC):
    """Стратегия получения данных"""
    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass


class DataUpdate(ABC):
    """Стратегия работы с данными"""
    @abstractmethod
    def update(self, data: Any) -> Any:
        pass


class DataExport(ABC):
    """Стратегия экспорта данных"""
    @abstractmethod
    def export(self, data: Any = None) -> Any:
        pass
