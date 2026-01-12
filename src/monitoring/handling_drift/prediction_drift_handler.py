import os
from dotenv import load_dotenv
from typing import Dict, List
from pathlib import Path
from src.monitoring.email_notifications.prediction_drift_email import PredictionDriftEmail
load_dotenv()

class PredictionDriftHandler:
    def __init__(self):
        self.notifier = PredictionDriftEmail(
            smtp_server = os.getenv("SMTP_SERVER"),
            smtp_port = os.getenv("SMTP_PORT"),
            sender_email = os.getenv("SENDER_EMAIL"),
            sender_password = os.getenv("SENDER_PASSWORD"),
            receiver_emails = os.getenv("RECEIVER_EMAILS")
        )

    def handle(self, prediction_result: Dict, prediction_paths: Dict) -> str:
        """
        Handles actions when prediction drift is detected.
        """

        if not prediction_result.get("drift_detected", False):
            print("No prediction drift detected")
            return "NO_PREDICTION_DRIFT"

        print("PREDICTION DRIFT DETECTED")

        drift_score = prediction_result.get("drift_score", None)
        if drift_score is not None:
            print(f"Prediction drift score: {drift_score}")
        
        attachments = [prediction_paths["json_path"],prediction_paths["html_path"]]
        self.notifier.send_drift_alert(
            subject = f"Prediction Drift Detected {drift_score}",
            attachments = attachments
        )

        return "PREDICTION_DRIFT_HANDLED"

