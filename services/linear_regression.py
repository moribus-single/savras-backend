import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from file import crud
from analysis import crud as ac
from sqlalchemy.orm import Session
import io
from os import path
import json


class LinearRegres:
    """Класс операций с линейной регрессией"""

    def get_result(self, fileid: int, db: Session):
        """ "Получение данных из БД."""
        result = json.loads(ac.get_result(fileid, db)[0])
        return result

    def save_to_db(self, fileid: int, result_dict: dict, db: Session):
        """Сохранение результатов LinearRegres в БД."""
        ac.save_result(fileid, result_dict, db)

    def make_df(self, fileid: int, db: Session):
        """Cчитывание бинарного файла в датафрейм."""
        file_name = f"data/linear_regression_{fileid}.xlsx"

        if not path.exists(file_name):
            byte_file = crud.get_file(fileid, db)
            write_obj = io.BytesIO()
            write_obj.write(byte_file[0])
            write_obj.seek(0)
            df = pd.read_excel(write_obj)
            df.to_excel(file_name)

        result_dict = self.linear_regression(file_name)
        self.save_to_db(fileid, result_dict, db)
        return result_dict

    def linear_regression(self, file_path: str):
        """Выполнение линейной регрессии."""
        excel_data_main = pd.read_excel(file_path)
        data_main = pd.DataFrame(excel_data_main)

        sort_data_main = data_main.loc[data_main["channel"] == "Чаты"]
        sort_data = sort_data_main.drop(
            columns=[
                "Unnamed: 0",
                "tm",
                "business_line",
                "sector",
                "channel",
                "skill_group",
                "avg_time_fact",
            ],
            axis=1,
        )

        x = sort_data.ds.unique()
        y = sort_data.groupby("ds")["load_fact"].sum()
        mydf = pd.DataFrame({"ds": x, "load": y})
        mydf["Time"] = np.arange(len(x))
        model = LinearRegression()
        x_train = pd.DataFrame(mydf.Time)
        y_train = pd.DataFrame(mydf.load)
        model.fit(x_train, y_train)
        y_result = model.predict(x_train)
        # print(X_train["Time"][0], y_result[0][0], X_train["Time"][-1], y_result[-1][0])
        model_score = model.score(x_train, y_train)
        return {
            "x_cord_first": x_train["Time"][0].item(),
            "x_cord_second": x_train["Time"][-1].item(),
            "y_cord_first": y_result[0][0].item(),
            "y_cord_second": y_result[-1][0].item(),
            "model_score": model_score.item(),
        }
