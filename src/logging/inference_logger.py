import pandas as pd
import os
from datetime import datetime
from config.settings import LIVE_DATA
from src.utils.schema_loader import SchemaLoader

class InferenceLogger:
    def __init__(self,model_version: str):
        self.model_version = model_version
        self.schema = SchemaLoader.load_schema()

        self.columns = (
            self.schema["features"]["categorical"] +
            self.schema["features"]["numerical"] +
            self.schema["metadata"] +
            ["prediction", "model_version", "timestamp"]
        )
    
    def log(self, input_data: dict, prediction: int):
        record = {
            **input_data,
            "prediction": prediction,
            "model_version": self.model_version,
            "timestamp": datetime.utcnow().isoformat()
        }

        df_new = pd.DataFrame([record])

        LIVE_DATA.parent.mkdir(parents=True, exist_ok=True)

        if not LIVE_DATA.exists() or LIVE_DATA.stat().st_size == 0:
            df_new.to_csv(LIVE_DATA, mode="w", header=True, index=False)
            return

        existing_cols = pd.read_csv(LIVE_DATA, nrows=0).columns.tolist()

        for col in existing_cols:
            if col not in df_new.columns:
                df_new[col] = None

        df_new = df_new[existing_cols]

        df_new.to_csv(LIVE_DATA, mode="a", header=False, index=False)
