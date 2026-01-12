import os
from dotenv import load_dotenv
from typing import Dict, List
from pathlib import Path
from src.monitoring.email_notifications.data_drift_email import DataDriftEmail
load_dotenv()

class DataDriftHandler:
    def __init__(self):
        self.notifier = DataDriftEmail(
            smtp_server = os.getenv("SMTP_SERVER"),
            smtp_port = os.getenv("SMTP_PORT"),
            sender_email = os.getenv("SENDER_EMAIL"),
            sender_password = os.getenv("SENDER_PASSWORD"),
            receiver_emails = os.getenv("RECEIVER_EMAILS")
        )

    def handle(self, drift_result: Dict) -> str:

        if not drift_result.get("dataset_drift", False):
            print("No significant data drift detected")
            return "NO_DATA_DRIFT"

        print("DATA DRIFT DETECTED")

        attachments = [drift_result["json_path"], drift_result["html_path"]]
        self.notifier.send_drift_alert(
            subject = "Data Drift Detected",
            drift_result = drift_result,
            attachments = attachments
        )

        drifted_columns = drift_result.get("drifted_columns", [])

        if drifted_columns:
            print("Drifted columns:")
            for col in drifted_columns:
                print(f" - {col}")

        return "DATA_DRIFT_HANDLED"