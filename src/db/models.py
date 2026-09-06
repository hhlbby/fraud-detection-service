from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String
from datetime import datetime
from src.db.database import Base

class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    amount = Column(Float, nullable=False)
    time_seconds = Column(Float, nullable=False)
    
    fraud_probability = Column(Float, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    model_version = Column(String, nullable=False)