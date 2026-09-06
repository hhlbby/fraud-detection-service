from pydantic import BaseModel, Field

class TransactionInput(BaseModel):
    Time: float = Field(..., ge=0, description="Время транзакции в секундах от начала отсчета")
    Amount: float = Field(..., ge=0, description="Сумма транзакции")
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    class Config:
        json_schema_extra = {
            "example": {
                "Time": 80000.0,
                "Amount": 150.0,
                **{f"V{i}": 0.0 for i in range(1, 29)}
            }
        }

class PredictionOutput(BaseModel):
    is_fraud: bool = Field(..., description="Флаг мошенничества (True/False)")
    fraud_probability: float = Field(..., ge=0.0, le=1.0, description="Вероятность фрода от 0 до 1")
    model_version: str = Field(..., description="Версия использованной модели")