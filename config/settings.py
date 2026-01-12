from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RUNTIME_DIR = Path(
    os.getenv("RUNTIME_DIR", "/tmp/churn_prediction")
)
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

SCHEMA_PATH = PROJECT_ROOT / "config" / "schemas.yaml"
MODEL_PATH = PROJECT_ROOT / "artifacts" / "rfc_tuned_model.joblib"
TRAINING_DATA = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "WA_Fn-UseC_-Telco-Customer-Churn 2.csv"
)

LIVE_DATA = RUNTIME_DIR / "live_data.csv"

MODEL_VERSION = "RFC_TUNED_V1"
