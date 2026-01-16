from sqlalchemy import Column, Integer, Float, TIMESTAMP, func
from app.db import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    prediction = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
