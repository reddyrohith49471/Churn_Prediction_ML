# import joblib
# import os

# MODEL_PATH = os.path.abspath("artifacts/rfc_tuned_model.joblib")

# print("MODEL PATH:", MODEL_PATH)
# print("EXISTS:", os.path.exists(MODEL_PATH))

# model = joblib.load(MODEL_PATH)

# print("MODEL TYPE:", type(model))
# print("MODEL:", model)


import pandas as pd
pd.set_option("display.max_columns",100)
training = pd.read_csv("data/reference/WA_Fn-UseC_-Telco-Customer-Churn 2.csv")
live = pd.read_csv("data/incoming/live_data.csv")
print(live.columns)

# from config.settings import BASE_DIR
# DRIFT_THRESHOLD_WARNING = 0.3
# DRIFT_THRESHOLD_SERVE = 0.5

# MIN_ROWS_REQUIRED = 100

# REPORT_DIR = BASE_DIR / "monitoring" / "data_reports"
# print(REPORT_DIR)






1. sending email 
2. segment wise drift
3. a/b testing
4. clean architecture diagram with readme.md
5. writing code in fastapi or flask
6. Deploying in render