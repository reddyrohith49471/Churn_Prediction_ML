import pandas as pd
from datetime import datetime
from config.settings import LIVE_DATA, TRAINING_DATA
from src.monitoring.config.drift_config import MIN_ROWS_REQUIRED, PREDICTION_REPORT_DIR
from src.monitoring.reports_builder.prediction_drift_report import PredictionDriftReport
from src.monitoring.handling_drift.prediction_drift_handler import PredictionDriftHandler


class PredictionDriftJob:
    def __init__(self):
        self.prediction_drift_report = PredictionDriftReport()
        self.prediction_drift_handler = PredictionDriftHandler()
    
    def run(self):
        reference_df = pd.read_csv(TRAINING_DATA)
        live_df = pd.read_csv(LIVE_DATA)

        if len(live_df) < MIN_ROWS_REQUIRED:
            return "Not enough live data for drift detection"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        prediction_result = self.prediction_drift_report.run_and_save(reference_df["Churn"],live_df["prediction"],PREDICTION_REPORT_DIR,timestamp)

        print("Prediction Drift Completed")

        prediction_drift_status = self.prediction_drift_handler.handle(prediction_result)

        return f"Prediction Drift Status: {prediction_drift_status}"



