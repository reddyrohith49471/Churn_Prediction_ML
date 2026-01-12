from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = BASE_DIR / "data"

SCHEMA_PATH = BASE_DIR / "config" / "schemas.yaml"
LIVE_DATA = BASE_DIR / "incoming" / "live_data.csv"
MODEL_PATH = BASE_DIR / "artifacts" / "rfc_tuned_model.joblib"

MODEL_VERSION = "RFC_TUNED_V1"

TRAINING_DATA = BASE_DIR / "reference" / "WA_Fn-UseC_-Telco-Customer-Churn 2.csv"
