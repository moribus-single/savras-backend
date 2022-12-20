from sqlalchemy import Column, Integer, String, JSON, LargeBinary, Float

from core.database import Base


class LinearReg(Base):
    __tablename__ = "linear_regression"

    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    result = Column(JSON)


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    with_anomaly = Column(LargeBinary)
    without_anomaly = Column(LargeBinary)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    predicts_number = Column(Integer)
    mae = Column(Float)
    mape = Column(Float)
    result = Column(LargeBinary)


class PredictionNeural(Base):
    __tablename__ = "predictions_neural"

    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    predicts_number = Column(Integer)
    mse = Column(Float)
    mape = Column(Float)
    result = Column(LargeBinary)
