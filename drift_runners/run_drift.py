from src.monitoring.drift_jobs.data_drift_job import DataDriftJob
from src.monitoring.drift_jobs.prediction_drift_job import PredictionDriftJob
from src.monitoring.drift_jobs.model_drift_job import ModelDriftJob

if __name__=="__main__":
    data_job = DataDriftJob()
    prediction_job = PredictionDriftJob()
    model_job = ModelDriftJob()
    print(data_job.run())
    print(prediction_job.run())
    print(model_job.run())