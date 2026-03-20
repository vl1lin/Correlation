import argparse
import sys
from pathlib import Path
from factory import CorrelationFactory


def main():
    parser = argparse.ArgumentParser(description="Генератор графиков корреляций свойств нефти")
    parser.add_argument("--correlation", type=str, required=True,
                        choices=["standing"],
                        help="Тип корреляции (пока доступен только 'standing')")
    parser.add_argument("--y-g", type=str, required=True,
                        help="Имя файла JSON с границами удельного веса газа")
    parser.add_argument("--temp", type=str, required=True,
                        help="Имя файла JSON с границами температуры")
    parser.add_argument("--api", type=str, required=True,
                        help="Имя файла JSON с границами API gravity")
    parser.add_argument("--rs", type=str, required=True,
                        help="Имя файла JSON с данными Rs")
    parser.add_argument("--output", type=str, default=None,
                        help="Имя выходного HTML файла")
    parser.add_argument("--no-show", action="store_true",
                        help="Не открывать браузер автоматически")
    parser.add_argument("--save-csv", type=str, default=None,
                        help="Сохранить отфильтрованные данные в CSV файл")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Директория с данными (по умолчанию ./data)")

    args = parser.parse_args()

    try:
        base_dir = Path(args.data_dir) if args.data_dir else None

        model = CorrelationFactory.create(
            name=args.correlation,
            path_y_g=args.y_g,
            path_temperature=args.temp,
            path_y_api=args.api,
            path_r_s=args.rs,
            base_dir=base_dir
        )

        df = model.filtration_data_p_b()

        if df.empty:
            print("Ошибка: После фильтрации не осталось данных (P_b <= 0). "
                  "Проверьте входные параметры.")
            sys.exit(1)

        print(f"Рассчитано {len(df)} точек данных.")

        show_browser = not args.no_show

        model.making_simple_plot(
            data_r_s=df["R_s"].tolist(),
            data_p_b=df["P_b"].tolist(),
            show=show_browser
        )

        if args.no_show or args.output:
            model.download_plot_to_html(filename=args.output)

        if args.save_csv:
            model.save_results_to_csv(file_path=args.save_csv)
            print(f"Данные сохранены в CSV: {args.save_csv}")

        else:
            print(f"Корреляция '{args.correlation}' пока не реализована.")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при выполнении: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
