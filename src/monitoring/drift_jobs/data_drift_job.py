from datetime import datetime
import pandas as pd
from config.settings import LIVE_DATA, TRAINING_DATA
from src.monitoring.config.drift_config import (
    DATA_REPORT_DIR,
    MIN_ROWS_REQUIRED,
    FEATURE_COLS,
    NUM_COLS,
    CAT_COLS
)
from src.monitoring.reports_builder.data_drift_report import DataDriftReport
from src.monitoring.handling_drift.data_drift_handler import DataDriftHandler


class DataDriftJob:
    def __init__(self):
        self.data_drift_report = DataDriftReport(NUM_COLS, CAT_COLS)
        self.data_drift_handler = DataDriftHandler()
        

    def run(self):
        reference_df = pd.read_csv(TRAINING_DATA)
        live_df = pd.read_csv(LIVE_DATA)

        if len(live_df) < MIN_ROWS_REQUIRED:
            return "Not enough live data for drift detection"

        reference_features = reference_df[FEATURE_COLS].copy()
        live_features = live_df[FEATURE_COLS].copy()

        reference_features["TotalCharges"] = pd.to_numeric(
            reference_features["TotalCharges"], errors="coerce"
        )
        live_features["TotalCharges"] = pd.to_numeric(
            live_features["TotalCharges"], errors="coerce"
        )
        print(reference_features["TotalCharges"].dtype)
        print(live_features["TotalCharges"].dtype)
        reference_features.dropna(inplace=True)
        live_features.dropna(inplace=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        
        data_drift_result = self.data_drift_report.run_and_save(reference_features, live_features, DATA_REPORT_DIR, timestamp)
        
        
        print("Data Drift Detection Completed Successfully")

        data_drift_status = self.data_drift_handler.handle(data_drift_result)

        return f"Data Drift Status: {data_drift_status}"

    
    
