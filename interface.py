from typing import Dict

from config import FEATURE_NAMES, FEATURE_LABELS


def show_menu() -> str:
    print("\n=== Система оценки кредитного риска ===")
    print("1 - Ввести данные клиента вручную")
    print("2 - Загрузить клиентов из CSV и сделать прогноз")
    print("3 - Показать последние результаты")
    print("4 - Выход")
    return input("Выберите пункт меню: ").strip()


def input_client_data() -> Dict[str, str]:
    print("\nВведите данные клиента:")
    client: Dict[str, str] = {}
    for feat in FEATURE_NAMES:
        label = FEATURE_LABELS.get(feat, feat)
        value = input(f"{label}: ").strip()
        client[feat] = value
    return client


def ask_csv_path() -> str:
    return input("\nВведите путь к CSV-файлу с клиентами: ").strip()


def ask_int(prompt: str, default: int) -> int:
    txt = input(f"{prompt} [{default}]: ").strip()
    if txt == "":
        return default
    try:
        return int(txt)
    except ValueError:
        print("Некорректное число, используется значение по умолчанию.")
        return default
