class DataDriftHandler:
    def __init__(self):
        pass

    def handle(self, drift_result: dict) -> str:
        """
        Handles actions when data drift is detected.
        """

        if not drift_result.get("dataset_drift", False):
            print("No significant data drift detected")
            return "NO_DATA_DRIFT"

        print("DATA DRIFT DETECTED")

        drifted_columns = drift_result.get("drifted_columns", [])

        if drifted_columns:
            print("Drifted columns:")
            for col in drifted_columns:
                print(f" - {col}")

        return "DATA_DRIFT_HANDLED"