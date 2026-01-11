class PredictionDriftHandler:
    def __init__(self):
        pass

    def handle(self, prediction_result: dict) -> str:
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

        return "PREDICTION_DRIFT_HANDLED"

