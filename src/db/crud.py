from sqlalchemy.orm import Session
from src.db.models import TransactionLog
from src.api.schemas import TransactionInput, PredictionOutput

def create_transaction_log(
    db: Session, 
    transaction: TransactionInput, 
    prediction: PredictionOutput
) -> TransactionLog:
    db_log = TransactionLog(
        amount=transaction.Amount,
        time_seconds=transaction.Time,
        fraud_probability=prediction.fraud_probability,
        is_fraud=prediction.is_fraud,
        model_version=prediction.model_version
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log