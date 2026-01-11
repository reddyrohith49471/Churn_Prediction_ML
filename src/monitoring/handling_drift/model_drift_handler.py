from datetime import datetime
from typing import Dict


class ModelDriftHandler:
    def __init__(
        self,
        warning_threshold: float = 0.15,
        critical_threshold: float = 0.25
    ):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def handle(self, drift_summary: Dict) -> Dict:
        if not drift_summary["drift_detected"]:
            return self._no_drift_response()

        severity = self._assess_severity(drift_summary["metric_analysis"])

        if severity == "CRITICAL":
            return self._critical_response(drift_summary)

        if severity == "WARNING":
            return self._warning_response(drift_summary)

        return self._no_drift_response()

    def _assess_severity(self, metric_analysis: Dict) -> str:
        max_drop = max(
            metric["relative_drop"]
            for metric in metric_analysis.values()
        )

        if max_drop >= self.critical_threshold:
            return "CRITICAL"

        if max_drop >= self.warning_threshold:
            return "WARNING"

        return "NONE"

    @staticmethod
    def _no_drift_response() -> Dict:
        return {
            "severity": "NONE",
            "action": "NO_ACTION",
            "message": "Model performance within acceptable limits"
        }

    @staticmethod
    def _warning_response(drift_summary: Dict) -> Dict:
        return {
            "severity": "WARNING",
            "action": "MONITOR_AND_ALERT",
            "message": "Model drift detected. Monitor closely.",
            "metrics": drift_summary["metric_analysis"],
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def _critical_response(drift_summary: Dict) -> Dict:
        return {
            "severity": "CRITICAL",
            "action": "TRIGGER_RETRAINING",
            "message": "Severe model drift detected. Retraining recommended.",
            "metrics": drift_summary["metric_analysis"],
            "timestamp": datetime.utcnow().isoformat()
        }
