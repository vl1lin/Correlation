import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from typing import Union, Optional
from abc import ABC, abstractmethod
from import_data import DataProcessor


class Correlation(ABC):
    def __init__(self, *,
                 path_y_g: Union[str, Path],
                 path_temperature: Union[str, Path],
                 path_y_api: Union[str, Path],
                 path_r_s: Union[str, Path],
                 base_dir: Optional[Path] = None) -> None:

        self._processor = DataProcessor(base_dir=base_dir)

        self._y_g = self._load_bounds(path_y_g)
        self._temperature = self._load_bounds(path_temperature)
        self._y_api = self._load_bounds(path_y_api)
        self._r_s_data = self._load_values(path_r_s)

        self.fig = go.Figure()
        self._processed_data: Optional[pd.DataFrame] = None

    def _load_bounds(self, file_name: Union[str, Path]) -> tuple:
        self._processor.load_file(file_name=file_name)
        return self._processor.get_bounds()

    def _load_values(self, file_name: Union[str, Path]) -> list:
        self._processor.load_file(file_name=file_name)
        return self._processor.get_values()

    @abstractmethod
    def data_correlation(self) -> pd.DataFrame:
        pass

    def making_simple_plot(self, *,
                           data_r_s: list,
                           data_p_b: list,
                           show: bool = True) -> None:
        self.fig.add_trace(go.Scatter(
            x=data_r_s,
            y=data_p_b,
            mode="lines+markers",
            name="Без учета границ применимости",
            line=dict(color="royalblue", width=2),
            marker=dict(size=8)
        ))
        self.fig.update_layout(
            title=f"Корреляция - {self.__class__.__name__}",
            xaxis_title="Rs (scf/STB)",
            yaxis_title="pb (psi)",
            template="plotly_white",
            hovermode="x unified"
        )
        if show:
            self.fig.show()
        else:
            filename = self.download_plot_to_html()
            print(f"График сохранен в файл: {filename}")

    def download_plot_to_html(self, filename: str = None) -> str:
        if filename is None:
            filename = f"static_{self.__class__.__name__}_plot.html"
        if not filename.endswith(".html"):
            filename += ".html"
        self.fig.write_html(filename)
        return filename

    def save_results_to_csv(self, *, file_path: Union[str, Path]) -> None:
        if self._processed_data is None:
            raise ValueError("Сначала выполните расчёт корреляции")
        self._processor._data = self._processed_data
        self._processor.save_file(file_path=file_path)

    @property
    def processor(self) -> DataProcessor:
        return self._processor
