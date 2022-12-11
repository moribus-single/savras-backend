from typing import List, AnyStr
from sqlalchemy.orm import Session
from file import crud


class LoaderService:
    """
    Allows to work with files in format CSV, XLSX
    """

    @staticmethod
    def load_csv(path: str) -> List[AnyStr]:
        with open(path, 'r') as file:
            return file.readlines()

    @staticmethod
    def load_xlsx(filename: str, content: bytes, db: Session):
        crud.load_file(filename, content, db)
        ...
