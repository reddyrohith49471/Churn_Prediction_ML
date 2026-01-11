from config.settings import BASE_DIR
DRIFT_THRESHOLD_WARNING = 0.3
DRIFT_THRESHOLD_SERVE = 0.5

MIN_ROWS_REQUIRED = 1

DATA_REPORT_DIR = BASE_DIR / "src" / "monitoring" / "drift_reports" / "data_reports"
PREDICTION_REPORT_DIR = BASE_DIR / "src" / "monitoring" / "drift_reports" / "prediction_reports"
MODEL_REPORT_DIR = BASE_DIR / "src" / "monitoring" / "drift_reports" / "model_reports"
REFERENCE_METRICS_PATH = MODEL_REPORT_DIR / "reference_model_drift" / "reference_model_metrics.json"
LIVE_METRICS_DIR =  MODEL_REPORT_DIR / "live_model_drift"

FEATURE_COLS = [
            "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
            "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
            "PaymentMethod", "MonthlyCharges", "TotalCharges"
        ]

NUM_COLS = [
    "TotalCharges", "MonthlyCharges", "tenure"
]

CAT_COLS = [
            "gender", "Partner", "Dependents",
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
            "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
            "PaymentMethod"
        ]