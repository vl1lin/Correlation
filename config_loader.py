import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


# --- DTO (Data Transfer Objects) ---


@dataclass
class InputPaths:
    y_g: str
    temperature: str
    api_gravity: str
    rs: str


@dataclass
class OutputConfig:
    plot_file: Optional[str] = None  # Куда сохранить график (HTML)
    csv_file: Optional[str] = None  # Куда сохранить таблицу (CSV)
    show_browser: bool = True  # Открывать ли браузер автоматически


@dataclass
class AppConfig:
    experiment_name: str  # Название эксперимента (для логов)
    model: str  # Имя модели (standing и т.д.)
    inputs: InputPaths  # Вложенный объект с путями
    output: OutputConfig = field(default_factory=OutputConfig)  # Вложенный объект с выводом

    # Метод класса для загрузки из YAML файла
    @classmethod
    def from_yaml(cls, file_path: str) -> 'AppConfig':
        path = Path(file_path)

        # Проверка существования файла конфига
        if not path.exists():
            raise FileNotFoundError(f"Конфигурационный файл не найден: {path}")

        # Чтение содержимого файла
        with path.open("r", encoding="utf-8") as f:
            try:
                # yaml.safe_load превращает текст YAML в обычный словарь Python (dict)
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Ошибка синтаксиса YAML: {e}")

        # Валидация обязательных полей (защита от опечаток в конфиге)
        if "model" not in data:
            raise ValueError("В конфиге отсутствует обязательное поле 'model'")
        if "inputs" not in data:
            raise ValueError("В конфиге отсутствует обязательный блок 'inputs'")

        # Извлечение вложенных данных с защитой от отсутствия ключей
        inputs_data = data["inputs"]
        required_inputs = ["y_g", "temperature", "api_gravity", "rs"]
        for key in required_inputs:
            if key not in inputs_data:
                raise ValueError(f"В блоке 'inputs' отсутствует путь к файлу: {key}")

        # Формирование итогового объекта AppConfig
        # Мы передаем словари внутрь классов данных, они сами распределят поля
        return cls(
            experiment_name=data.get("experiment_name", "Unnamed_Experiment"),
            model=data["model"],
            inputs=InputPaths(**inputs_data),  # Распаковка словаря в аргументы класса
            output=OutputConfig(**data.get("output", {}))  # Если блока output нет, будут дефолтные значения
        )
