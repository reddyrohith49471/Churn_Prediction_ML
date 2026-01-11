import joblib
from src.config.config import MODEL_PATH

class ModelLoader:
    _model = None

    @classmethod
    def load_model(cls):
        print("Loading Model:",MODEL_PATH)
        if cls._model is None:
            cls._model = joblib.load(MODEL_PATH)
            print("Model Loaded:", type(cls._model))
        return cls._model