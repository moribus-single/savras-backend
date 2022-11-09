from typing import List, AnyStr


class LoaderService:
    """
    Allows to work with files in format CSV, XLSX
    """

    @staticmethod
    def load_csv(path: str) -> List[AnyStr]:
        with open(path, 'r') as file:
            return file.readlines()

    @staticmethod
    def load_xlsx(path: str) -> List[AnyStr]:
        with open(path, 'r') as file:
            return file.readlines()
