import json
from pathlib import Path
import pandas as pd

from sklearn.metrics import precision_score, recall_score, f1_score

from src.monitoring.config.drift_config import (
    MODEL_REPORT_DIR,
    LIVE_METRICS_DIR,
    REFERENCE_METRICS_PATH
)
from src.monitoring.reports_builder.base_report import BaseReport


class ModelDriftReport(BaseReport):
    def __init__(self, target_col: str, prediction_col: str):
        self.target_col = target_col
        self.prediction_col = prediction_col

    def run_and_save(
        self,
        live_df: pd.DataFrame,
        report_dir: Path,
        timestamp: str
    ) -> dict:

        self._validate_columns(live_df)

        live_metrics = self._compute_metrics(live_df)
        ref_metrics = self._load_or_create_reference_metrics(live_metrics)

        self._save_live_metrics(live_metrics, timestamp)

        drift_summary = self._detect_drift(ref_metrics, live_metrics)

        report = {
            "type": "model_drift",
            "timestamp": timestamp,
            "reference_metrics": ref_metrics,
            "live_metrics": live_metrics,
            "drift_summary": drift_summary
        }

        report_dir.mkdir(parents=True, exist_ok=True)
        self._save_report(report, report_dir, timestamp)

        report_path = report_dir
        return drift_summary, report_path

    def _compute_metrics(self, df: pd.DataFrame) -> dict:
        y_true = df[self.target_col]
        y_pred = df[self.prediction_col]

        return {
            "precision": round(precision_score(y_true, y_pred, pos_label=1), 4),
            "recall": round(recall_score(y_true, y_pred, pos_label=1), 4),
            "f1_score": round(f1_score(y_true, y_pred, pos_label=1), 4)
        }

    @staticmethod
    def _validate_columns(df: pd.DataFrame):
        required = ["Churn", "prediction"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Live data missing required column: {col}")

    @staticmethod
    def _load_or_create_reference_metrics(live_metrics: dict) -> dict:
        REFERENCE_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

        if REFERENCE_METRICS_PATH.exists():
            if REFERENCE_METRICS_PATH.is_dir():
                raise IsADirectoryError(
                    f"REFERENCE_METRICS_PATH is a directory: {REFERENCE_METRICS_PATH}"
                )

            with open(REFERENCE_METRICS_PATH, "r") as f:
                return json.load(f)

        with open(REFERENCE_METRICS_PATH, "w") as f:
            json.dump(live_metrics, f, indent=4)

        return live_metrics

    @staticmethod
    def _detect_drift(
        ref: dict,
        live: dict,
        threshold: float = 0.15
    ) -> dict:
        drift_metrics = {}
        drift_detected = False

        for metric in ref:
            relative_drop = (ref[metric] - live[metric]) / max(ref[metric], 1e-6)

            drift_metrics[metric] = {
                "reference": ref[metric],
                "live": live[metric],
                "relative_drop": round(relative_drop, 4)
            }

            if relative_drop >= threshold:
                drift_detected = True

        return {
            "drift_detected": drift_detected,
            "threshold": threshold,
            "metric_analysis": drift_metrics
        }

    @staticmethod
    def _save_report(report: dict, report_dir: Path, timestamp: str):
        path = report_dir / f"model_drift_{timestamp}.json"
        with open(path, "w") as f:
            json.dump(report, f, indent=4)

    @staticmethod
    def _save_live_metrics(live_metrics: dict, timestamp: str):
        LIVE_METRICS_DIR.mkdir(parents=True, exist_ok=True)

        path = LIVE_METRICS_DIR / f"live_metrics_{timestamp}.json"
        with open(path, "w") as f:
            json.dump(
                {
                    "timestamp": timestamp,
                    "metrics": live_metrics
                },
                f,
                indent=4
            )
