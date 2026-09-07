import json
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd
from catboost import CatBoostClassifier


class FraudModelService:

    def __init__(
        self,
        model_path: str = "models/catboost_fraud_v1.cbm",
        scaler_path: str = "models/scaler.joblib",
        metadata_path: str = "models/metadata.json",
    ):
        self.model_path = Path(model_path)
        self.scaler_path = Path(scaler_path)
        self.metadata_path = Path(metadata_path)

        self._validate_paths()
        self._load_artifacts()

    def _validate_paths(self) -> None:
        for path in (self.model_path, self.scaler_path, self.metadata_path):
            if not path.exists():
                raise FileNotFoundError(
                    f"Артефакт не найден по пути: {path.resolve()}"
                )

    def _load_artifacts(self) -> None:
        self.model = CatBoostClassifier()
        self.model.load_model(str(self.model_path))

        self.scaler = joblib.load(self.scaler_path)

        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.threshold: float = float(self.metadata["optimal_threshold"])
        self.feature_names: list[str] = self.metadata["feature_names"]
        self.scaled_features: list[str] = self.metadata.get(
            "scaled_features", ["Time", "Amount"]
        )

    def predict(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        df = pd.DataFrame([transaction_data])

        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0.0

        df = df[self.feature_names]

        df[self.scaled_features] = self.scaler.transform(
            df[self.scaled_features]
        )

        proba = float(self.model.predict_proba(df)[0, 1])
        is_fraud = proba >= self.threshold

        return {
            "is_fraud": is_fraud,
            "fraud_probability": round(proba, 4),
            "threshold_used": self.threshold,
            "model_version": self.metadata.get("model_version", "v1"),
        }
