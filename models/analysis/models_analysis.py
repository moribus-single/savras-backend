from sqlalchemy import Column, Integer, Float

from core.database import Base


class LinearReg(Base):
    __tablename__ = "linear_regression"
    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    x_cord_first = Column(Float)
    y_cord_first = Column(Float)
    x_cord_second = Column(Float)
    y_cord_second = Column(Float)
    model_score = Column(Float)
