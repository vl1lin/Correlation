import json
import numpy as np
import pandas as pd
import random
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, Union
from pathlib import Path


class FileStrategy(ABC):
    def read(self, *, file_path: Union[str, Path]) -> None:
        pass

    def write(self, *, data: pd.DataFrame, file_path_to_write: Union[Path, str]) -> None:
        pass


class JsonStrategy(FileStrategy):
    pass