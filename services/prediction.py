import pandas as pd
import numpy as np
from plotly import graph_objs as go
import plotly as plotly
import prophet
from models.file import crud_file as cf
from models.analysis import crud_analysis as ca
from sqlalchemy.orm import Session
from os import path
import io


class Prediction:
    def get_result(self, fileid: int, db: Session):
        """Получение результатов прогнозирования по сохранённым .xlsx файлам."""
        return f"data/prediction_{fileid}.xlsx"

    def save_to_db(
        self,
        fileid: int,
        predictions: int,
        mae: int,
        mape: int,
        result: bytes,
        db: Session,
    ):
        """Сохранение результатов Prediction в БД."""
        ca.save_result_pr(fileid, predictions, mae, mape, result, db)

    def make_df(self, fileid: int, predictions: int, db: Session):
        """Cчитывание бинарного файла в датафрейм для Prediction."""
        file_name = f"data/sample_{fileid}.xlsx"

        if not path.exists(file_name):
            byte_file = cf.get_file(fileid, db)
            write_obj = io.BytesIO()
            write_obj.write(byte_file[0])
            write_obj.seek(0)
            df = pd.read_excel(write_obj)
            df.to_excel(file_name)

        excel_data_main = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data_main)
        data = data.drop(columns=["Unnamed: 0.1"], axis=1)

        result = self.predict(fileid, predictions, data)
        self.save_to_db(fileid, predictions, result[0], result[1], result[2], db)
        return self.get_result(fileid, db)

    def predict(self, fileid: int, predictions: int, data: pd.DataFrame):
        """Функция прогнозирования по датафрейму."""
        sort_data_main = data.loc[data["channel"] == "Чаты"].drop(
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
        df = sort_data_main.reset_index()
        df.columns = ["", "ds", "y"]
        df = df.drop(columns=[""], axis=1)

        train_df = df[:-predictions]

        # Прогнозируем
        m = prophet.Prophet()
        m.fit(train_df)
        future = m.make_future_dataframe(periods=predictions)
        forecast = m.predict(future)

        # Смотрим на ошибки модели
        cmp_df = forecast.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]].join(
            df.set_index("ds")
        )
        cmp_df["e"] = cmp_df["y"] - cmp_df["yhat"]
        cmp_df["p"] = 100 * cmp_df["e"] / cmp_df["y"]
        mape = np.mean(abs(cmp_df[-30:]["p"]))
        mae = np.mean(abs(cmp_df[-30:]["e"]))

        # Визуализация
        fig = go.Figure()
        visualise = [
            go.Scatter(x=df["ds"], y=df["y"], name="fact"),
            go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="prediction"),
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_upper"],
                fill="tonexty",
                mode="none",
                name="upper",
            ),
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_lower"],
                fill="tonexty",
                mode="none",
                name="lower",
            ),
            go.Scatter(x=forecast["ds"], y=forecast["trend"], name="trend"),
        ]
        fig.add_traces(visualise)
        fig.write_image(f"visualisation/prediction_{fileid}.png")

        forecast.to_excel(f"data/prediction_{fileid}.xlsx")

        with open(f"data/prediction_{fileid}.xlsx", "rb") as file:
            forecast_b = file.read()

        return mae, mape, forecast_b
