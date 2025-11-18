import csv
from typing import List, Dict

from config import FEATURE_NAMES, RESULTS_FILE


def read_clients_from_csv(path: str) -> List[Dict[str, str]]:
    clients: List[Dict[str, str]] = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clients.append(row)
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл {path} не найден.")
    except Exception as e:
        print(f"[ОШИБКА] При чтении {path}: {e}")
    return clients


def append_result_to_file(
    client_data: dict, model_results: dict, path: str = RESULTS_FILE
) -> None:
    """
    Добавить строки с результатами в CSV.
    Одна строка = один клиент + одна модель.
    """
    fieldnames = FEATURE_NAMES + ["model", "prob_default", "risk_level"]

    file_exists = False
    try:
        with open(path, "r", encoding="utf-8") as _:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    try:
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            for model_name, res in model_results.items():
                row = {feat: client_data.get(feat, "") for feat in FEATURE_NAMES}
                row.update(
                    {
                        "model": model_name,
                        "prob_default": f"{res['prob_default']:.4f}",
                        "risk_level": res["risk_level"],
                    }
                )
                writer.writerow(row)
    except Exception as e:
        print(f"[ОШИБКА] Не удалось записать в файл {path}: {e}")


def show_last_results(path: str = RESULTS_FILE, n: int = 10) -> None:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        print("[ИНФО] Файл с результатами пока не создан.")
        return
    except Exception as e:
        print(f"[ОШИБКА] Не удалось прочитать {path}: {e}")
        return

    if len(rows) <= 1:
        print("[ИНФО] В файле нет данных.")
        return

    header, data_rows = rows[0], rows[1:]
    print(f"\nПоследние {min(n, len(data_rows))} записей из {path}:")
    for row in data_rows[-n:]:
        print("-" * 40)
        for h, v in zip(header, row):
            print(f"{h}: {v}")
