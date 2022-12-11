from sqlalchemy import Column, Integer, String, ARRAY, LargeBinary

from core.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True)
    content = Column(LargeBinary)
