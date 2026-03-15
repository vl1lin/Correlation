import argparse
import sys
from models.Standing import Standing


def main():
    parser = argparse.ArgumentParser(description="Генератор графиков корреляций свойств нефти")

    parser.add_argument("--correlation", type=str, required=True, choices=["standing"],
                        help="Тип корреляции (пока доступен только 'standing')")
    parser.add_argument("--y-g", type=str, required=True, help="Путь к JSON с границами удельного веса газа")
    parser.add_argument("--temp", type=str, required=True, help="Путь к JSON с границами температуры")
    parser.add_argument("--api", type=str, required=True, help="Путь к JSON с границами API gravity")
    parser.add_argument("--rs", type=str, required=True, help="Путь к JSON с данными Rs")

    parser.add_argument("--output", type=str, default=None,
                        help="Имя выходного HTML файла")
    parser.add_argument("--no-show", action="store_true",
                        help="Не открывать браузер автоматически")
    parser.add_argument("--save-csv", type=str, default=None,
                        help="Сохранить отфильтрованные данные в CSV файл")

    args = parser.parse_args()

    try:
        if args.correlation == "standing":
            model = Standing(
                path_y_g=args.y_g,
                path_temperature=args.temp,
                path_y_api=args.api,
                path_r_s=args.rs
            )

            df = model.filtration_data_p_b()

            if df.empty:
                print("Ошибка: После фильтрации не осталось данных (P_b <= 0). Проверьте входные параметры.")
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
                df.to_csv(args.save_csv, index=False)
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
