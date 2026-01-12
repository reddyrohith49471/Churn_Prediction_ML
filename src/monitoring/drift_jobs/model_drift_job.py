import pandas as pd
from datetime import datetime

from config.settings import LIVE_DATA
from src.monitoring.config.drift_config import (
    MODEL_REPORT_DIR,
    MIN_ROWS_REQUIRED
)
from src.monitoring.reports_builder.model_drift_report import ModelDriftReport
from src.monitoring.handling_drift.model_drift_handler import ModelDriftHandler


class ModelDriftJob:
    def __init__(self):
        self.model_drift_report = ModelDriftReport(
            target_col="Churn",
            prediction_col="prediction"
        )
        self.model_drift_handler = ModelDriftHandler()

    def run(self) -> dict:
        live_df = pd.read_csv(LIVE_DATA)

        if len(live_df) < MIN_ROWS_REQUIRED:
            return {
                "status": "SKIPPED",
                "reason": "Not enough live data"
            }

        live_df = self._clean_live(live_df)

        if "Churn" not in live_df.columns:
            return {
                "status": "SKIPPED",
                "reason": "Ground truth not available yet for model drift"
            }

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        drift_summary, drift_path = self.model_drift_report.run_and_save(
            live_df=live_df,
            report_dir=MODEL_REPORT_DIR,
            timestamp=timestamp
        )

        handling_decision = self.model_drift_handler.handle(drift_summary, drift_path)

        return {
            "status": "COMPLETED",
            "drift_summary": drift_summary,
            "handling_decision": handling_decision
        }

    @staticmethod
    def _clean_live(df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(columns=["model_version", "timestamp"], errors="ignore")
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        return df.dropna()
