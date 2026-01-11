import pandas as pd
from src.logging.inference_logger import InferenceLogger
from src.core.model_loader import ModelLoader
from config.settings import MODEL_VERSION

class InferenceService:
    def __init__(self):
        self.model = ModelLoader.load_model()
        self.logger = InferenceLogger(model_version=MODEL_VERSION)

    def predict(self, input_data: dict) -> int:
        df = pd.DataFrame([input_data])
        prediction = int(self.model.predict(df)[0])

        self.logger.log(
            input_data = input_data,
            prediction = prediction
        )

        return prediction
