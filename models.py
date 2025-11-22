from typing import Dict, Any

import numpy as np
import joblib
import pandas as pd  

from config import MODEL_PATHS, FEATURE_NAMES, risk_level


def load_models() -> Dict[str, Any]:
    """Загрузка всех моделей из .pkl через joblib."""
    models = {}
    for name, path in MODEL_PATHS.items():
        try:
            model = joblib.load(path)
            models[name] = model
            print(f"[OK] Модель '{name}' загружена из {path}")
        except FileNotFoundError:
            print(
                f"[ПРЕДУПРЕЖДЕНИЕ] Файл модели {path} не найден. "
                f"Модель '{name}' не будет использоваться."
            )
        except Exception as e:
            print(f"[ОШИБКА] Не удалось загрузить модель '{name}' из {path}: {e}")

    if not models:
        raise RuntimeError(
            "Не удалось загрузить ни одной модели. "
            "Проверь пути к .pkl в config.py и формат сохранения (joblib.dump)."
        )
    return models


def _dict_to_vector(client_data: dict) -> np.ndarray:
    vector = []
    for feat in FEATURE_NAMES:
        if feat not in client_data:
            raise ValueError(f"Отсутствует признак '{feat}' в данных клиента")
        try:
            value = float(client_data[feat])
        except ValueError:
            raise ValueError(
                f"Невозможно преобразовать '{feat}' "
                f"к числу: {client_data[feat]}"
            )
        vector.append(value)

    return np.array([vector], dtype=float)


def predict_for_client(models: Dict[str, Any], client_data: dict) -> Dict[str, dict]:
    """
    Формируем DataFrame с теми же именами признаков, что и при обучении:
    колонки = FEATURE_NAMES
    """
    row = []
    for feat in FEATURE_NAMES:
        if feat not in client_data:
            raise ValueError(f"Отсутствует признак '{feat}' в данных клиента")
        try:
            value = float(client_data[feat])
        except ValueError:
            raise ValueError(
                f"Невозможно преобразовать '{feat}' "
                f"к числу: {client_data[feat]}"
            )
        row.append(value)

    X = pd.DataFrame([row], columns=FEATURE_NAMES)

    results: Dict[str, dict] = {}

    for name, model in models.items():
        if not hasattr(model, "predict_proba"):
            raise AttributeError(f"У модели '{name}' нет метода predict_proba")

        proba_default = float(model.predict_proba(X)[0, 1])

        results[name] = {
            "prob_default": proba_default,
            "risk_level": risk_level(proba_default),
        }

    return results
