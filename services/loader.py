from typing import List, AnyStr
from sqlalchemy.orm import Session
import pandas as pd
from file import crud


class LoaderService:
    """
    Allows to work with files in format CSV, XLSX
    """

    @staticmethod
    def load_csv(filename: str, content: bytes, db: Session):
        crud.load_file(filename, content, db)
        ...

    @staticmethod
    def load_xlsx(filename: str, content: bytes, db: Session):
        crud.load_file(filename, content, db)
        ...
