import json
import numpy as np
from scipy.stats import chi2_contingency
from src.monitoring.reports_builder.base_report import BaseReport


class PredictionDriftReport(BaseReport):
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.report = {}

    def run_and_save(self, reference_df, live_df, report_dir, timestamp):
        report_dir.mkdir(parents=True, exist_ok=True)
        reference_df = reference_df.map({"No":0,"Yes":1})
        reference_df = reference_df.astype(int)
        live_df = live_df.dropna()
        live_df = live_df.astype(int)

        ref_counts = np.bincount(reference_df)
        live_counts = np.bincount(live_df)

        max_len = max(len(ref_counts), len(live_counts))
        ref_counts = np.pad(ref_counts, (0, max_len - len(ref_counts)))
        live_counts = np.pad(live_counts, (0, max_len - len(live_counts)))

        contingency_table = np.vstack([ref_counts, live_counts])

        chi2, p_value, _, _ = chi2_contingency(contingency_table)

        self.report = {
            "type": "prediction_drift",
            "method": "chi_square",
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "alpha": float(self.alpha),
            "drift_detected": bool(p_value < self.alpha),
            "reference_distribution": ref_counts.tolist(),
            "live_distribution": live_counts.tolist(),
        }

    
        json_path = report_dir / f"{timestamp}_prediction_drift.json"
        html_path = report_dir / f"{timestamp}_prediction_drift.html"
        self.paths = {
            "json_path": json_path,
            "html_path": html_path
        }


        with open(json_path, "w") as f:
            json.dump(self.report, f, indent=4)

        html_content = f"""
        <html>
        <head><title>Prediction Drift Report</title></head>
        <body>
            <h2>Prediction Drift Report</h2>
            <p><b>Method:</b> Chi-Square Test</p>
            <p><b>Chi-Square Statistic:</b> {self.report['chi2_statistic']}</p>
            <p><b>P-Value:</b> {self.report['p_value']}</p>
            <p><b>Alpha:</b> {self.report['alpha']}</p>
            <p><b>Drift Detected:</b> {self.report['drift_detected']}</p>

            <h3>Label Distribution</h3>
            <p><b>Reference:</b> {self.report['reference_distribution']}</p>
            <p><b>Live:</b> {self.report['live_distribution']}</p>
        </body>
        </html>
        """

        with open(html_path, "w") as f:
            f.write(html_content)

        return self.report, self.paths

