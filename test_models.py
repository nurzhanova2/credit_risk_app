import numpy as np
import pandas as pd
import joblib

from config import FEATURE_NAMES  

paths = [
    "models/log_reg.pkl",          
    "models/random_forest.pkl",    
    "models/xgboost.pkl",        
]

for p in paths:
    try:
        model = joblib.load(p)
        print(f"[OK] {p} загружен: {type(model)}")

        x = np.zeros((1, len(FEATURE_NAMES)))

        X = pd.DataFrame(x, columns=FEATURE_NAMES)

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            print("    predict_proba работает, shape:", proba.shape)
        else:
            print("    ВНИМАНИЕ: у модели нет predict_proba")
    except FileNotFoundError:
        print(f"[MISS] {p} не найден")
    except Exception as e:
        print(f"[ERROR] {p}: {e}")
