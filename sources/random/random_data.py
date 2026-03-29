import random
from typing import Any
from Correlation_mini_app.technical_files.interfaces import DataSources
import pandas as pd


class GenerateData(DataSources):
    def fetch(self) -> pd.DataFrame:
        pass
