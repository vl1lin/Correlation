import argparse
import sys
from pathlib import Path
from Correlation_mini_app.technical_files.factory import CorrelationFactory
from Correlation_mini_app.terminal_loader.config_loader import InputPaths, OutputConfig, AppConfig


def run_application(config: AppConfig):

    print(f"Запуск эксперимента: {config.experiment_name}")
    print(f"Модель: {config.model}")

    try:
        # 1. Создание модели через Фабрику
        # Передаем base_dir, чтобы модель знала, где искать файлы, если пути относительные
        # Если base_dir не указан в конфиге, можно передать None или Path.cwd()
        # base_dir = getattr(config, 'base_dir', None)

        model = CorrelationFactory.create(
            name=config.model,
            path_y_g=config.inputs.y_g,
            path_temperature=config.inputs.temperature,
            path_y_api=config.inputs.api_gravity,
            path_r_s=config.inputs.rs,
            # base_dir=base_dir
        )

        # 2. Расчет данных
        df = model.filtration_data_p_b()

        if df.empty:
            print("Ошибка: После фильтрации не осталось данных (P_b <= 0).")
            sys.exit(1)

        print(f"Рассчитано {len(df)} точек данных.")

        # 3. Построение графика
        show_browser = config.output.show_browser

        model.making_simple_plot(
            data_r_s=df["R_s"].tolist(),
            data_p_b=df["P_b"].tolist(),
            show=show_browser
        )

        # 4. Сохранение результатов
        # создаем папки, если они не существуют
        if config.output.plot_file:
            Path(config.output.plot_file).parent.mkdir(parents=True, exist_ok=True)
            model.download_plot_to_html(filename=config.output.plot_file)
            print(f"График сохранен: {config.output.plot_file}")

        if config.output.csv_file:
            Path(config.output.csv_file).parent.mkdir(parents=True, exist_ok=True)
            # Предполагаем, что вы добавили метод save_results_to_csv в класс Correlation
            # Если нет, используйте df.to_csv(...) напрямую
            if hasattr(model, 'save_results_to_csv'):
                model.save_results_to_csv(file_path=config.output.csv_file)
            else:
                df.to_csv(config.output.csv_file, index=False)
            print(f"💾 CSV сохранен: {config.output.csv_file}")

    except Exception as e:
        print(f"💥 Критическая ошибка при выполнении: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Генератор графиков корреляций свойств нефти")
    # 1. Флаг конфига (всегда опционален для парсера)
    parser.add_argument("--config", type=str,
                        help="Путь к YAML файлу конфигурации. Если указан, остальные флаги игнорируются.")

    # 2. Ручные флаги (ТОЖЕ опциональны для парсера, required убираем!)
    parser.add_argument("--correlation", type=str, choices=["standing"],
                        help="Тип корреляции")
    parser.add_argument("--y-g", type=str, help="Путь к JSON y_g")
    parser.add_argument("--temp", type=str, help="Путь к JSON температуры")
    parser.add_argument("--api", type=str, help="Путь к JSON API")
    parser.add_argument("--rs", type=str, help="Путь к JSON Rs")

    # Опции вывода
    parser.add_argument("--output", type=str, default=None, help="Имя выходного HTML файла")
    parser.add_argument("--no-show", action="store_true", help="Не открывать браузер")
    parser.add_argument("--save-csv", type=str, default=None, help="Сохранить в CSV")
    parser.add_argument("--data-dir", type=str, default=None, help="Базовая директория данных")

    args = parser.parse_args()

    # --- ЛОГИКА ВЫБОРА РЕЖИМА ---

    if args.config:
        # РЕЖИМ 1: Загрузка из YAML конфигурации
        if not Path(args.config).exists():
            print(f"❌ Ошибка: Файл конфигурации не найден: {args.config}")
            sys.exit(1)

        try:
            # Загружаем DTO из файла
            config = AppConfig.from_yaml(args.config)

            # Переопределение отдельных настроек из командной строки (если нужно)
            # Например, если в конфиге show_browser=True, но вы запустили с --no-show
            if args.no_show:
                config.output.show_browser = False
            if args.output:
                config.output.plot_file = args.output
            if args.save_csv:
                config.output.csv_file = args.save_csv
            if args.data_dir:
                config.base_dir = Path(args.data_dir)

            run_application(config)

        except (FileNotFoundError, ValueError) as e:
            print(f"❌ Ошибка чтения конфигурации: {e}")
            sys.exit(1)

    else:
        # РЕЖИМ 2: Ручной запуск (старый способ)
        # Проверяем, все ли обязательные аргументы указаны
        required_manual = [args.correlation, args.y_g, args.temp, args.api, args.rs]
        if not all(required_manual):
            print("❌ Ошибка: В режиме без конфига необходимо указать все параметры:")
            print("   --correlation, --y-g, --temp, --api, --rs")
            print("   Либо используйте флаг --config file.yaml")
            sys.exit(1)

        # Собираем ручной конфиг в DTO
        manual_config = AppConfig(
            experiment_name="Manual_Run",
            model=args.correlation,
            inputs=InputPaths(
                y_g=args.y_g,
                temperature=args.temp,
                api_gravity=args.api,
                rs=args.rs
            ),
            output=OutputConfig(
                plot_file=args.output,
                csv_file=args.save_csv,
                show_browser=not args.no_show
            )
        )

        run_application(manual_config)


if __name__ == "__main__":
    main()
