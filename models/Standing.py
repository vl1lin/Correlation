from Correlation_mini_app.models.core import Correlation
import random
import numpy as np
import pandas as pd


class Standing(Correlation):
    coefficient_dict = {"a": 18.2, "b": 0.83, "c": 0.00091, "d": 0.0125, "e": 1.4}

    def data_correlation(self) -> np.ndarray:
        data_y_g = np.arange(self._y_g[0], self._y_g[1], 10)
        data_y_api = np.arange(self._y_api[0], self._y_api[1], 10)
        data_temperature = np.arange(self._temperature[0], self._temperature[1], 10)

        try:
            if len(data_y_g) == 0 or len(data_y_api) == 0 or len(data_temperature) == 0:
                raise ValueError("Диапазон параметров слишком мал для выбора случайного значения с шагом 10.")

            y_g = random.choice(data_y_g)
            y_api = random.choice(data_y_api)
            temperature = random.choice(data_temperature)
        except ValueError as e:
            print(f"Предупреждение: {e}. Используются средние значения.")
            # Защита от IndexError, если массив пуст
            y_g = (self._y_g[0] + self._y_g[1]) / 2 if len(data_y_g) == 0 else random.choice(data_y_g)
            y_api = (self._y_api[0] + self._y_api[1]) / 2 if len(data_y_api) == 0 else random.choice(data_y_api)
            temperature = (self._temperature[0] + self._temperature[1]) / 2 if len(
                data_temperature) == 0 else random.choice(data_temperature)

        term_power = (self._r_s_data / y_g) ** self.coefficient_dict["b"]
        exponent = self.coefficient_dict["c"] * temperature - self.coefficient_dict["d"] * y_api
        term_exp = 10 ** exponent

        p_b_data = self.coefficient_dict["a"] * (term_power * term_exp - self.coefficient_dict["e"])
        return p_b_data

    def filtration_data_p_b(self) -> pd.DataFrame:
        pb = self.data_correlation().flatten()
        data = pd.DataFrame({
            "R_s": np.array(self._r_s_data).flatten(),
            "P_b": pb
        })
        valid_data = data[data["P_b"] > 0].copy()
        return valid_data
