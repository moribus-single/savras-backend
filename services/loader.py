from sqlalchemy.orm import Session
from models.file import crud_file as crud


class LoaderService:
    """Allows to work with files in format CSV, XLSX."""

    @staticmethod
    def load_csv(filename: str, content: bytes, db: Session):
        fileid = crud.load_file(filename, content, db)
        return fileid

    @staticmethod
    def load_xlsx(filename: str, content: bytes, db: Session):
        fileid = crud.load_file(filename, content, db)
        return fileid
