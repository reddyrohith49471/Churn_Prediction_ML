import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List
from pathlib import Path

class PredictionDriftEmail:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str, receiver_emails: List[str]):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_emails = [e.strip() for e in receiver_emails.split(",") if e.strip()]

    def send_drift_alert(self, subject: str, attachments: List[Path] | None = None):

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.receiver_emails)
        message["Subject"] = subject

        body = self._build_email_body()

        message.attach(MIMEText(body, "plain"))

        if attachments:
            for file_path in attachments:
                self._attach_file(message, file_path)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_email,self.sender_password)
            server.sendmail(
                from_addr = self.sender_email,
                to_addrs = self.receiver_emails,
                msg = message.as_string()
            )

    
    @staticmethod
    def _build_email_body() -> str:
        return "Prediction Drift Detected"

    @staticmethod
    def _attach_file(message: MIMEMultipart, file_path: Path):
        if not file_path.exists():
            return

        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{file_path.name}"'
        )
        message.attach(part)