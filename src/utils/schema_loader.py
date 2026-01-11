import yaml
from config.settings import SCHEMA_PATH

class SchemaLoader:
    _schema = None

    @classmethod
    def load_schema(cls):
        if cls._schema is None:
            with open(SCHEMA_PATH, "r") as f:
                cls._schema = yaml.safe_load(f)
        return cls._schema