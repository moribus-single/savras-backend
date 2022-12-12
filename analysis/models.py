from sqlalchemy import Column, Integer, String, JSON

from core.database import Base


class LinearReg(Base):
    __tablename__ = "linear_regression"
    id = Column(Integer, primary_key=True, index=True)
    fileid = Column(Integer, unique=True)
    result = Column(JSON)
