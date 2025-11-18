# main.py
from models import load_models, predict_for_client
from io_utils import (
    read_clients_from_csv,
    append_result_to_file,
    show_last_results,
)
from interface import show_menu, input_client_data, ask_csv_path, ask_int


def main():
    try:
        models = load_models()
    except Exception as e:
        print(f"Критическая ошибка при загрузке моделей: {e}")
        return

    # Основной цикл меню
    while True:
        choice = show_menu()

        if choice == "1":
            # Ввод одного клиента
            client = input_client_data()
            try:
                results = predict_for_client(models, client)
            except Exception as e:
                print(f"[ОШИБКА] Не удалось сделать прогноз: {e}")
                continue

            print("\nРезультаты прогноза:")
            for name, res in results.items():
                print(f"- Модель: {name}")
                print(f"  Вероятность дефолта: {res['prob_default']:.4f}")
                print(f"  Уровень риска: {res['risk_level']}")

            append_result_to_file(client, results)

        elif choice == "2":
            # Пакетная обработка из CSV
            path = ask_csv_path()
            clients = read_clients_from_csv(path)
            if not clients:
                print("Клиенты не найдены или файл пустой/ошибочный.")
                continue

            print(f"Найдено клиентов: {len(clients)}")
            for i, client in enumerate(clients, start=1):
                print(f"\nКлиент #{i}")
                try:
                    results = predict_for_client(models, client)
                except Exception as e:
                    print(f"[ОШИБКА] Не удалось сделать прогноз для клиента #{i}: {e}")
                    continue

                for name, res in results.items():
                    print(
                        f"- {name}: p(default)={res['prob_default']:.4f}, "
                        f"риск={res['risk_level']}"
                    )
                append_result_to_file(client, results)

        elif choice == "3":
            # Просмотр последних N результатов
            n = ask_int("Сколько последних записей показать?", 10)
            show_last_results(n=n)

        elif choice == "4":
            print("Выход из программы. Пока!")
            break

        else:
            print("Неизвестный пункт меню, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
