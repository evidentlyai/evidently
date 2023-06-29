from typing import Callable, Optional, Text

import joblib


class ModelLoader:
    """Model loader singleton."""

    _instance: Optional[object] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.model_path: Text = 'models/model.joblib'
        self.model: Optional[Callable] = None

    def get_model(self) -> Callable:

        if not self.model:
            self._load_model()

        return self.model

    def _load_model(self) -> None:
        self.model = joblib.load(self.model_path)
