from evidently import Report
from evidently.presets import DataDriftPreset
import pandas as pd
import json
from pathlib import Path

from src.monitoring.reports_builder.base_report import BaseReport
from src.monitoring.config.drift_config import DATA_REPORT_DIR


class DataDriftReport(BaseReport):
    def __init__(self, num_cols, cat_cols):
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.report: Report | None = None

    def run_and_save(self, reference_df: pd.DataFrame, live_df: pd.DataFrame, report_dir: Path, timestamp: str):
        self.report = Report(
            metrics=[DataDriftPreset()]
        )

        
        self.my_eval = self.report.run(
            reference_data=reference_df,
            current_data=live_df
        )

        report_dir.mkdir(parents=True, exist_ok=True)
        json_path = report_dir / f"data_drift_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(
                json.loads(self.my_eval.json()),
                f,
                indent=4
            )

        html_path = report_dir / f"data_drift_{timestamp}.html"
        print(html_path)
        self.my_eval.save_html(str(html_path))

        return self._extract_drift_summary(json.loads(self.my_eval.json()), json_path, html_path)

    
    def _extract_drift_summary(self, report_json: dict, json_path: Path, html_path: Path) -> dict:
        drifted_columns = []

        for metric in report_json["metrics"]:
            if "ValueDrift" in metric["metric_name"]:
                value = metric["value"]
                threshold = metric["config"]["threshold"]
                column = metric["config"]["column"]

                if value > threshold:
                    drifted_columns.append(column)

        dataset_drift = False

        for metric in report_json["metrics"]:
            if metric["metric_name"].startswith("DriftedColumnsCount"):
                dataset_drift = metric["value"]["share"] >= 0.5

        return {
            "dataset_drift": dataset_drift,
            "drifted_columns": drifted_columns,
            "drifted_count": len(drifted_columns),
            "json_path": json_path,
            "html_path": html_path
        }

