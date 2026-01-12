from src.monitoring.drift_jobs.data_drift_job import DataDriftJob
from src.monitoring.drift_jobs.prediction_drift_job import PredictionDriftJob
from src.monitoring.drift_jobs.model_drift_job import ModelDriftJob


def run_all_drifts():
    data_job = DataDriftJob()
    prediction_job = PredictionDriftJob()
    model_job = ModelDriftJob()

    results = {
        "data_drift": data_job.run(),
        "prediction_drift": prediction_job.run(),
        "model_drift": model_job.run()
    }

    return results


if __name__ == "__main__":
    results = run_all_drifts()
    print(results)
