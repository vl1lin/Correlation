import json
import plotly.graph_objects as go
from pathlib import Path
from typing import Union, Dict, Any
from abc import ABC, abstractmethod
import numpy as np


class Correlation(ABC):
    def __init__(self, *,
                 path_y_g: Union[str, Path],
                 path_temperature: Union[str, Path],
                 path_y_api: Union[str, Path],
                 path_r_s: Union[str, Path]) -> None:
        self._y_g = self.load_bounds(file_path=path_y_g)
        self._temperature = self.load_bounds(file_path=path_temperature)
        self._y_api = self.load_bounds(file_path=path_y_api)
        self._r_s_data = self.converting_from_dict_to_list(parameter_path=path_r_s)
        self.fig = go.Figure()

    @staticmethod
    def get_data_from_json(*, file_path: Union[str, Path]) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")
        try:
            with path.open("r", encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка формата JSON: {e}")
        return data

    @staticmethod
    def converting_from_dict_to_list(*, parameter_path: Union[str, Path]) -> np.ndarray:
        data_list = Correlation.get_data_from_json(file_path=parameter_path)["values"]
        return np.array(data_list)

    @staticmethod
    def load_bounds(*, file_path: Union[str, Path]) -> tuple:
        data = Correlation.get_data_from_json(file_path=file_path)
        data_tuple = (data["lower_bound"], data["upper_bound"])
        return data_tuple

    @abstractmethod
    def data_correlation(self):
        pass

    def making_simple_plot(self, *, data_r_s: list, data_p_b: list, show: bool = True) -> None:
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
        # Добавлено расширение .html, если его нет
        if not filename.endswith(".html"):
            filename += ".html"
        self.fig.write_html(filename)
        return filename

    def making_animated_plot(self):
        pass
