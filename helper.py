import os
from config.settings import LIVE_DATA
from src.monitoring.config.drift_config import MIN_ROWS_REQUIRED
from src.core.inference_service import InferenceService


class ChurnService:
    def __init__(self):
        self.predictor = InferenceService()

    def predict(self, input_data: dict) -> int:
        return self.predictor.predict(input_data)

    def log_inference(self, input_data: dict):

        os.makedirs(os.path.dirname(LIVE_DATA), exist_ok=True)

        file_exists = os.path.exists(LIVE_DATA)

        with open(LIVE_DATA, "a") as f:
            if not file_exists:
                f.write(",".join(input_data.keys()) + "\n")
            f.write(",".join(map(str, input_data.values())) + "\n")

    def get_live_row_count(self) -> int:
        try:
            with open(LIVE_DATA, "r") as f:
                return sum(1 for _ in f) - 1
        except FileNotFoundError:
            return 0

    def maybe_trigger_drift(self):
        row_count = self.get_live_row_count()

        print(f"[DRIFT CHECK] Live rows = {row_count}, Threshold = {MIN_ROWS_REQUIRED}")

        if row_count >= MIN_ROWS_REQUIRED:
            print("[DRIFT CHECK] Threshold reached. Running drift...")
            self.run_drift()
        else:
            print("[DRIFT CHECK] Threshold NOT reached. Skipping drift.")
            
    def run_drift(self):
        from drift_runners.run_drift import run_all_drifts
        run_all_drifts()
