FEATURE_NAMES = [
    "person_age",
    "person_income",
    "person_emp_length",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "cb_person_cred_hist_length",
    "person_home_ownership_OTHER",
    "person_home_ownership_OWN",
    "person_home_ownership_RENT",
    "loan_intent_EDUCATION",
    "loan_intent_HOMEIMPROVEMENT",
    "loan_intent_MEDICAL",
    "loan_intent_PERSONAL",
    "loan_intent_VENTURE",
    "loan_grade_B",
    "loan_grade_C",
    "loan_grade_D",
    "loan_grade_E",
    "loan_grade_F",
    "loan_grade_G",
    "cb_person_default_on_file_Y",
]

FEATURE_LABELS = {
    "person_age": "Возраст клиента (лет)",
    "person_income": "Годовой доход клиента (USD)",
    "person_emp_length": "Стаж работы (лет)",
    "loan_amnt": "Сумма кредита (USD)",
    "loan_int_rate": "Процентная ставка по кредиту (%)",
    "loan_percent_income": "Платёж по кредиту / доход (доля)",
    "cb_person_cred_hist_length": "Длина кредитной истории (лет)",

    # Категориальные признаки (One-Hot)
    "person_home_ownership_OTHER": "Тип жилья: другое (0 = нет, 1 = да)",
    "person_home_ownership_OWN": "Тип жилья: собственное (0 = нет, 1 = да)",
    "person_home_ownership_RENT": "Тип жилья: аренда (0 = нет, 1 = да)",

    "loan_intent_EDUCATION": "Цель кредита: образование (0 = нет, 1 = да)",
    "loan_intent_HOMEIMPROVEMENT": "Цель кредита: ремонт (0 = нет, 1 = да)",
    "loan_intent_MEDICAL": "Цель кредита: лечение (0 = нет, 1 = да)",
    "loan_intent_PERSONAL": "Цель кредита: личные нужды (0 = нет, 1 = да)",
    "loan_intent_VENTURE": "Цель кредита: бизнес (0 = нет, 1 = да)",

    "loan_grade_B": "Кредитный рейтинг B (0 = нет, 1 = да)",
    "loan_grade_C": "Кредитный рейтинг C (0 = нет, 1 = да)",
    "loan_grade_D": "Кредитный рейтинг D (0 = нет, 1 = да)",
    "loan_grade_E": "Кредитный рейтинг E (0 = нет, 1 = да)",
    "loan_grade_F": "Кредитный рейтинг F (0 = нет, 1 = да)",
    "loan_grade_G": "Кредитный рейтинг G (0 = нет, 1 = да)",

    "cb_person_default_on_file_Y": "Были ли дефолты в прошлом (0 = нет, 1 = да)",
}


MODEL_PATHS = {
    "LogisticRegression": "models/log_reg.pkl",
    "RandomForest": "models/random_forest.pkl",
    "XGBoost": "models/xgboost.pkl",
}

RESULTS_FILE = "results.csv"

def risk_level(prob_default: float) -> str:
    """
    Классификация уровня риска по вероятности дефолта.
    Пороговые значения можно подстроить под анализ.
    """
    if prob_default < 0.15:
        return "Низкий"
    elif prob_default < 0.40:
        return "Средний"
    else:
        return "Высокий"
